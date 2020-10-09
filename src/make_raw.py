import json

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
    file = open(output_raw+".csv","w")
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
    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
         json.dump(uk_al, outfile, indent=4)
    return uk_al



def get_forbidden_bead(df_eplet_file, stronger_eplet_on_link, positive_bead, allele_type, mfi):

    allele_forbid = {}
    allele_forbid[allele_type+"_stronger"] = []

    all_stronger = set()
    for couple, eplets in stronger_eplet_on_link.items():
        for eplet in eplets:
            all_stronger.add(eplet)

    forbidden_bead = {}
    for eplet in all_stronger:
        forbidden_bead[eplet] = []


    for eplet in all_stronger:
        for allele in df_eplet_file.index:
            if eplet in list(df_eplet_file.loc[allele]):
                if allele not in positive_bead:
                    forbidden_bead[eplet].append(allele)

    allele_forbid[allele_type+"_stronger"].append(forbidden_bead)
    with open('result/json/{}.json'.format(mfi.split(".")[0])) as data_file:
        old_data = json.load(data_file)

        json_dict = {}
        json_dict["main"] = []
        json_dict["main"].append(old_data)
        json_dict["main"].append(allele_forbid)

    with open('result/json/{}.json'.format(mfi.split(".")[0]), 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)

