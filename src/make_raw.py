import json
import pandas as pd

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
    if allele_type in "A B C DR":
        allele_forbid = {}
        allele_forbid[allele_type+"_stronger"] = []

        all_stronger = set()
        for couple, eplets in stronger_eplet_on_link.items():
            for eplet in eplets:
                all_stronger.add(eplet)
        for bead,eplets in stronger_eplet_on_bead.items():
            for eplet in eplets:
                all_stronger.add(eplet)
        forbidden_bead = {}
        for eplet in all_stronger:
            forbidden_bead[eplet] = []


        for eplet in all_stronger:
            for allele in df_eplet_file.index:
                if eplet in list(df_eplet_file.loc[allele]):
                    if allele not in positive_bead:
                        forbidden_bead[eplet].append([allele, False])
                    else:
                        forbidden_bead[eplet].append([allele, True])

        allele_forbid[allele_type+"_stronger"].append(forbidden_bead)

    elif allele_type in "DQ DP":
        allele_forbid = {}
        allele_forbid[allele_type + "_stronger"] = []

        new_positive_bead = []
        for i in positive_bead:
            new_positive_bead.append(i[0:10])
            new_positive_bead.append(i[10:])

        all_stronger = set()
        for couple, eplets in stronger_eplet_on_link.items():
            for eplet in eplets:
                all_stronger.add(eplet)

        for bead,eplets in stronger_eplet_on_bead.items():
            for eplet in eplets:
                all_stronger.add(eplet)

        forbidden_bead = {}
        for eplet in all_stronger:
            forbidden_bead[eplet] = []

        df_eplet_file = pd.read_csv("data/eplets/{}_eplets.csv".format(allele_type)).set_index("allele")
        for eplet in all_stronger:
            for allele in df_eplet_file.index:
                if eplet in list(df_eplet_file.loc[allele]):
                    if allele not in new_positive_bead:
                        forbidden_bead[eplet].append([allele, False])
                    else:
                        forbidden_bead[eplet].append([allele, True])

        allele_forbid[allele_type + "_stronger"].append(forbidden_bead)

    with open('result/json/{}.json'.format(mfi.split(".")[0])) as data_file:
            old_data = json.load(data_file)
            old_data["main"].append(allele_forbid)


    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
            json.dump(old_data, outfile, indent=4)

def get_forbidden_bead_light(df_eplet_file, strong_eplet_on_link, strong_eplet_on_bead, positive_bead, allele_type, mfi):

    if allele_type in "A B C DR":
        allele_forbid = {}
        allele_forbid[allele_type+"_strong"] = []

        all_strong = set()
        for couple, eplets in strong_eplet_on_link.items():
            for eplet in eplets:
                all_strong.add(eplet)
        for bead,eplets in strong_eplet_on_bead.items():
            for eplet in eplets:
                all_strong.add(eplet)
        forbidden_bead = {}
        for eplet in all_strong:
            forbidden_bead[eplet] = []


        for eplet in all_strong:
            for allele in df_eplet_file.index:
                if eplet in list(df_eplet_file.loc[allele]):
                    if allele not in positive_bead:
                        forbidden_bead[eplet].append([allele, False])
                    else:
                        forbidden_bead[eplet].append([allele, True])

        allele_forbid[allele_type+"_strong"].append(forbidden_bead)

    elif allele_type in "DQ DP":
        allele_forbid = {}
        allele_forbid[allele_type + "_strong"] = []

        new_positive_bead = []
        for i in positive_bead:
            new_positive_bead.append(i[0:10])
            new_positive_bead.append(i[10:])


        all_strong = set()
        for couple, eplets in strong_eplet_on_link.items():
            for eplet in eplets:
                all_strong.add(eplet)

        for bead,eplets in strong_eplet_on_bead.items():
            for eplet in eplets:
                all_strong.add(eplet)

        forbidden_bead = {}
        for eplet in all_strong:
            forbidden_bead[eplet] = []

        df_eplet_file = pd.read_csv("data/eplets/{}_eplets.csv".format(allele_type)).set_index("allele")
        for eplet in all_strong:
            for allele in df_eplet_file.index:
                if eplet in list(df_eplet_file.loc[allele]):
                    if allele not in new_positive_bead:
                        forbidden_bead[eplet].append([allele, False])
                    else :
                        forbidden_bead[eplet].append([allele, True])

        allele_forbid[allele_type + "_strong"].append(forbidden_bead)

    with open('result/json/{}.json'.format(mfi.split(".")[0])) as data_file:
            old_data = json.load(data_file)
            old_data["main"].append(allele_forbid)


    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
            json.dump(old_data, outfile, indent=4)

    return 'result/json/{}.json'.format(mfi.split(".")[0])

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
                            global_dict[eplet+"stronger"] = allele
                        else :
                            global_dict[eplet + "strong"] = allele

        global_dict = sorted_dict_by_true_eplet(global_dict)
        df = pd.DataFrame.from_dict(global_dict, orient="index")
        df.replace(to_replace=[None], value="", inplace=True)
        df = df.transpose()

        # output_file("result/html_table/{}.html".format(json_file.split("/")[2].split(".")[0]))
        # Columns = [TableColumn(field=Ci, title=Ci, width=350) for Ci in df.columns]  # bokeh columns
        # data_table = DataTable(columns=Columns, source=ColumnDataSource(df), width=900, height=450, fit_columns=True)  # bokeh table
        # save(data_table)

        return df

def make_html_file(df, output):
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
