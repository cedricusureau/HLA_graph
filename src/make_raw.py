import json
from typing import Dict, Any

import pandas as pd
import time

def make_raw_data(final_fonction):
    stronger_eplet_on_link, strong_eplet_on_link, stronger_eplet_on_bead, strong_eplet_on_bead = final_fonction[0],final_fonction[1],final_fonction[2],final_fonction[3]

    all_stronger = {}
    all_strong = {}

    for couple,eplets in stronger_eplet_on_link.items():
        for eplet in eplets:
            bead1 = couple.split(" ")[0]
            bead2 = couple.split(" ")[1]

            if bead1 not in all_stronger.keys():
                all_stronger[bead1] = set()
                all_stronger[bead1].add(eplet)
            else:
                all_stronger[bead1].add(eplet)

            if bead2 not in all_stronger.keys():
                all_stronger[bead2] = set()
                all_stronger[bead2].add(eplet)
            else:
                all_stronger[bead2].add(eplet)

    for bead, eplets in stronger_eplet_on_bead.items():
        for eplet in eplets:
            if bead not in all_stronger.keys():
                all_stronger[bead] = set()
                all_stronger[bead].add(eplet)
            else:
                all_stronger[bead].add(eplet)

    for couple, eplets in strong_eplet_on_link.items():
        for eplet in eplets:
            bead1 = couple.split(" ")[0]
            bead2 = couple.split(" ")[1]

            if bead1 not in all_strong.keys():
                all_strong[bead1] = set()
                all_strong[bead1].add(eplet)
            else:
                all_strong[bead1].add(eplet)

            if bead2 not in all_strong.keys():
                all_strong[bead2] = set()
                all_strong[bead2].add(eplet)
            else:
                all_strong[bead2].add(eplet)

    for bead, eplets in strong_eplet_on_bead.items():
        for eplet in eplets:
            if bead not in all_strong.keys():
                all_strong[bead] = set()
                all_strong[bead].add(eplet)
            else:
                all_strong[bead].add(eplet)

    return all_stronger, all_strong

def write_all_raw_data(all_raw_data, output_raw):

    file = open(output_raw+".csv","a")
    for allele, raw_data in all_raw_data:
        stronger = raw_data[0]
        strong = raw_data[1]
        file.write("Eplets from HLA-{} bead\n".format(allele))
        for i,j in stronger.items():
            file.write(str(i)+",")
            for eplet in j:
                file.write(eplet+",")
                if i in strong.keys():
                    for eplet2 in strong[i]:
                        file.write(str(eplet2) + ",")
            file.write("\n")
        for i,j in strong.items():
            if i not in stronger.keys():
                file.write(str(i)+',')
                for eplet in j:
                    file.write(eplet+",")
                file.write("\n")

        #
        # file.write("Eplets from HLA-{} beads. These eplets are present on some of the positive bead \n".format(allele))
        # for i,j in strong.items():
        #     file.write(i+",")
        #     for eplet in j:
        #         file.write(eplet+",")
        #     file.write("\n")

    file.close()


def write_json(data, filename):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)


def write_json_unknown(unknown_allele, mfi):
    uk_al = {}
    uk_al["Unknown_allele"] = []

    uk_by_type = {}

    for i in unknown_allele:
        if "DR" in i :
            uk_by_type["DR"] = i
        elif "DP" in i :
            uk_by_type["DP"] = i
        elif "DQ" in i :
            uk_by_type["DQ"] = i
        elif "A*" in i:
            uk_by_type["A"] = i
        elif "B*" in i :
            uk_by_type["B"] = i
        elif "C*" in i :
            uk_by_type["C"] = i

    uk_al["Unknown_allele"].append(uk_by_type)
    whole_json = {}
    whole_json["main"] = []
    whole_json["main"].append(uk_al)
    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
         json.dump(whole_json, outfile, indent=4)

def get_forbidden_bead(df_eplet_file, stronger_eplet_on_link, stronger_eplet_on_bead, positive_bead, allele_type, mfi):


    if 'DQ' in allele_type or "DP" in allele_type:
        positive_bead = reformate_DQDP_pos_bead(positive_bead)

    if "A" in allele_type or "B" in allele_type or "C" in allele_type:
        df_all_eplet = pd.read_csv("data/eplet_to_allele/eplet_to_allele_C1.csv")
    else:
        df_all_eplet = pd.read_csv("data/eplet_to_allele/eplet_to_allele_C2.csv")

    all_stronger_ep = [i for i in stronger_eplet_on_link.values()] + [i for i in stronger_eplet_on_bead.values()]
    ep_set = set()

    for ls in all_stronger_ep:
        for ep in ls:
            ep_set.add(ep)

    allele_forbid = {}
    allele_forbid[allele_type+"_stronger"] = []

    forbidden_bead = {}
    for eplet in ep_set:
        forbidden_bead[eplet] = []

    for eplet in ep_set:
        for i in [i for i in list(df_all_eplet[eplet]) if str(i) !="nan"] :
            if i in positive_bead:
                forbidden_bead[eplet].append([i, True])
            else:
                forbidden_bead[eplet].append([i, False])

    allele_forbid[allele_type+"_stronger"].append(forbidden_bead)

    with open('result/json/{}.json'.format(mfi.split(".")[0])) as data_file:
            old_data = json.load(data_file)
            old_data["main"].append(allele_forbid)

    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
            json.dump(old_data, outfile, indent=4)

def get_forbidden_bead_light(df_eplet_file, strong_eplet_on_link, strong_eplet_on_bead, positive_bead, allele_type, mfi):
    if "A" in allele_type or "B" in allele_type or "C" in allele_type:
        df_all_eplet = pd.read_csv("data/eplet_to_allele/eplet_to_allele_C1.csv")
    else:
        df_all_eplet = pd.read_csv("data/eplet_to_allele/eplet_to_allele_C2.csv")

    if 'DQ' in allele_type or "DP" in allele_type:
        positive_bead = reformate_DQDP_pos_bead(positive_bead)

    all_stronger_ep = [i for i in strong_eplet_on_link.values()] + [i for i in strong_eplet_on_bead.values()]
    ep_set = set()

    for ls in all_stronger_ep:
        for ep in ls:
            ep_set.add(ep)

    allele_forbid = {}
    allele_forbid[allele_type + "_strong"] = []

    forbidden_bead = {}
    for eplet in ep_set:
        forbidden_bead[eplet] = []


    for eplet in ep_set:
        try:
            for i in [i for i in list(df_all_eplet[eplet]) if str(i) !="nan"] :
                if i in positive_bead:
                    forbidden_bead[eplet].append([i, True])
                else:
                    forbidden_bead[eplet].append([i, False])
        except:

            (eplet)

    allele_forbid[allele_type + "_strong"].append(forbidden_bead)

    with open('result/json/{}.json'.format(mfi.split(".")[0])) as data_file:
        old_data = json.load(data_file)
        old_data["main"].append(allele_forbid)

    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
        json.dump(old_data, outfile, indent=4)

def parse_json_to_html(json_file):
    with open(json_file) as data_file:
        json_to_parse = json.load(data_file)
        global_dict = {}
        eplets = json_to_parse["main"][1:]

        for dico in eplets:
            for name, liste in dico.items():
                for element in liste:
                    for eplet, allele in element.items():
                        if "stronger" in name:
                            global_dict[eplet+"stronger"] = []
                        else :
                            global_dict[eplet + "strong"] = []

        for dico in eplets:
            for name, liste in dico.items():
                for element in liste:
                    for eplet, allele in element.items():
                        for element in allele:
                            if "stronger" in name:
                                if element not in global_dict[eplet+"stronger"]:
                                    global_dict[eplet+"stronger"].append(element)
                            else :
                                if element not in global_dict[eplet+"strong"]:
                                    global_dict[eplet + "strong"].append(element)

        global_dict = put_strong_in_stronger(global_dict)
        global_dict = sorted_dict_by_true_eplet(global_dict)

        df = pd.DataFrame.from_dict(global_dict, orient="index")
        df.replace(to_replace=[None], value="", inplace=True)

        df = df.transpose()


        return df

def make_html_file(df, output):

    df = ordering_light_df(df)
    template_liste = [i for i in open("data/html_table_template/html_table.html","r")]
    for i, ligne in enumerate(template_liste):
        if "<tr>" in ligne :
            first_tr = i
            break

    template_liste.insert(first_tr+1, write_column(df))

    for i, ligne in enumerate(template_liste):
        if "<tbody>" in ligne:
            first_tbody = i
            break

    count2 = 0
    for i in range(df.shape[0]):
        template_liste.insert(int(first_tbody)+1+count2, "<tr>")
        template_liste.insert(int(first_tbody)+2+count2, write_ligne(df.iloc[i]))
        template_liste.insert(int(first_tbody)+3+count2, "</tr>\n")
        count2+=3

    file = open(output, "w")
    for ligne in template_liste:
        file.write(ligne)
    file.close()

def make_html_file_light(df, output):

    df = reformate_df(df)

    df = ordering_light_df(df)

    template_liste = [i for i in open("data/html_table_template/html_table.html","r")]
    for i, ligne in enumerate(template_liste):
        if "<tr>" in ligne :
            first_tr = i
            break

    template_liste.insert(first_tr+1, write_column(df))

    for i, ligne in enumerate(template_liste):
        if "<tbody>" in ligne:
            first_tbody = i
            break

    count2 = 0
    for i in range(df.shape[0]):
        template_liste.insert(int(first_tbody)+1+count2, "<tr>")
        template_liste.insert(int(first_tbody)+2+count2, write_ligne_light(df.iloc[i]))
        template_liste.insert(int(first_tbody)+3+count2, "</tr>\n")
        count2+=3

    file = open(output, "w")
    for ligne in template_liste:
        file.write(ligne)
    file.close()


def sorted_dict_by_true_eplet(dico):
    sorted_dict = {}

    for eplet in dico.keys():
        sorted_dict[eplet] = []

    for eplet, beads_list in dico.items():
        for bead in beads_list:
            if bead[1] == True:
                sorted_dict[eplet].append(bead)

    for eplet, beads_list in dico.items():
        for bead in beads_list:
            if bead[1] == False:
                sorted_dict[eplet].append(bead)

    return sorted_dict

def write_ligne(panda_series):
    whole_str = ""
    for i in list(panda_series):

        if type(i) == list:
            if i[1]:
                whole_str += '<td class="table-active">{}</td>'.format(i[0])
            else :
                whole_str += '<td class="table-warning">{}</td>'.format(i[0])
        else :
            whole_str += '<td> </td>'

    return whole_str

def write_ligne_light(panda_series):

    whole_str = ""
    for i in list(panda_series):
        if type(i) == list:
            if i[1]:
                whole_str += '<td class="table-active">{}</td>'.format(i[0])
            else:
                whole_str += '<td> </td>'
        else :
            whole_str += '<td> </td>'

    return whole_str

def write_column(df):
    whole_str = ""
    for i in list(df.columns):
        if "stronger" in i:
            whole_str += '<td class = "table-danger">{}</td>'.format(i.replace("stronger",""))
        else :
            whole_str += '<td class = "table-success">{}</td>'.format(i.replace("strong",""))

    return whole_str

def reorder_column(df):
    columns = df.columns.tolist()

    new_col_order = []
    for i in columns:
        if "stronger" in i:
            new_col_order.append(i)
    for i in columns:
        if "stronger" not in i :
             new_col_order.append(i)

    df = df[new_col_order]
    return df

def reformate_DQDP_pos_bead(positive_bead):
    new_liste = []
    for i in positive_bead:
        new_liste.append(i[:10])
        new_liste.append(i[10:])

    return new_liste

def check_true_in_row(pandas_series):
    for element in pandas_series:
        try:
            if element[1] == 1:
                return True
        except:
            pass

    return False

def reformate_df(df):

    bool_l = []

    for i in df.index:
        pandas_series = df.loc[i]
        bool_l.append(check_true_in_row(pandas_series))

    df = df[bool_l]
    return df

def put_strong_in_stronger(global_dict):
    to_pop = []
    for i in global_dict.keys():
            if "stronger" in i:
                tmp = i.replace("stronger","")
                for i2 in global_dict.keys():
                    if i2 == tmp+"strong":
                        to_pop.append(i2)
                        tmp_list = global_dict[i]

                        for strong in global_dict[i2]:
                            tmp_list.append(strong)

                        global_dict[i] = tmp_list

    for i in to_pop:
        global_dict.pop(i, None)

    return global_dict

def ordering_light_df(df):

    count_true_in_columns: Dict[Any, int] = {}

    for i in df.columns:
        true_nb = len([j for j in [k for k in df[i] if len(k) == 2] if j[1] == True])
        count_true_in_columns[i] = true_nb

    count_true_in_columns = {k: v for k, v in sorted(count_true_in_columns.items(), key=lambda item: item[1], reverse=True)}

    df = df[list(count_true_in_columns.keys())]

    new_df = {}
    for i in df.columns:
        a = [j for j in [k for k in df[i] if len(k) == 2] if j[1] == True]
        b = sorted([j[0] for j in a])
        e = [element for element, _ in sorted(zip(a, b))]

        c = [j for j in [k for k in df[i] if len(k) == 2] if j[1] == False]
        f = sorted([j[0] for j in c])
        g = [element for element, _ in sorted(zip(c, f))]

        new_col = e + g

        new_df[i] = new_col

    df = pd.DataFrame.from_dict(new_df, orient='index').transpose()

    new_order = []
    for i in df.columns:
        if "stronger" in i:
            new_order.append(i)

    for i in df.columns:
        if "stronger" not in i:
            if "strong" in i:
                new_order.append(i)

    df = df[new_order]
    return df