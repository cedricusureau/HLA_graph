import pandas as pd

def parse_eplet_file(eplet_path):
    df_eplet_file = pd.read_csv(eplet_path).set_index("allele")
    return df_eplet_file

def get_eplets_list_from_beads(bead_name, df_eplet_file):
    return [i for i in list(df_eplet_file.loc[bead_name]) if type(i) == str]

def get_beads_statut(data, cutoff, allele_type):


    positive_beads = []
    ambiguous_bead = []
    negative_bead = []
    for bead, mfi_value in data.items():
        if allele_type in bead:
            if mfi_value > cutoff:
                positive_beads.append(bead)

            elif mfi_value < cutoff & mfi_value > 1000:
                ambiguous_bead.append(bead)
                negative_bead.append(bead)
            else :
                negative_bead.append(bead)
    print(negative_bead)
    return positive_beads, ambiguous_bead, negative_bead

def get_bead_and_eplet_to_write(positive_bead, negative_bead, df_eplet_file):
    eplet_carried_by_negative_bead = set()


    for bead in negative_bead:

        for eplet in get_eplets_list_from_beads(bead,df_eplet_file):
            eplet_carried_by_negative_bead.add(eplet)


    eplet_not_carried_by_negative_bead = []
    for bead in positive_bead:
        for eplet in get_eplets_list_from_beads(bead, df_eplet_file):
            if eplet not in eplet_carried_by_negative_bead:
                eplet_not_carried_by_negative_bead.append(eplet)

    always_present_eplet = set()
    not_always_present_eplet = set()

    for eplet in eplet_not_carried_by_negative_bead:
        still_true = True
        for bead in positive_bead:
            tmp_eplet_liste = get_eplets_list_from_beads(bead,df_eplet_file)
            if eplet in tmp_eplet_liste:
                continue
            else :
                not_always_present_eplet.add(eplet)
                still_true = False
        if still_true == True:
            always_present_eplet.add(eplet)

    always_present_eplet_dict = {}
    not_always_present_eplet_dict = {}

    for bead in positive_bead:
        always_present_eplet_dict[bead] = []
        not_always_present_eplet_dict[bead] = []

    for bead in positive_bead:
        tmp_eplet_liste = get_eplets_list_from_beads(bead,df_eplet_file)
        for eplet in always_present_eplet:
            if eplet in tmp_eplet_liste:
                always_present_eplet_dict[bead].append(eplet)
        for eplet in not_always_present_eplet:
            if eplet in tmp_eplet_liste:
                not_always_present_eplet_dict[bead].append(eplet)

    return always_present_eplet, not_always_present_eplet, always_present_eplet_dict, not_always_present_eplet_dict

def get_positive_but_not_linked(link_between_pos, positive_bead):
    positive_linked = set()
    for i in link_between_pos:
        positive_linked.add(i.split(" ")[0])
        positive_linked.add(i.split(" ")[1])

    positive_not_linked = []
    for i in positive_bead:
        if i not in positive_linked:
            positive_not_linked.append(i)
    return positive_not_linked

def where_to_write_eplets(link_between_pos, always_present_eplet, not_always_present_eplet, always_present_eplet_dict, not_always_present_eplet_dict, positive_bead, positive_not_linked):
    stronger_eplet_on_link = {}
    strong_eplet_on_link = {}

    for linked in link_between_pos:
        stronger_eplet_on_link[linked] = []
        strong_eplet_on_link[linked] = []

    stronger_eplet_on_bead = {}
    strong_eplet_on_bead = {}


    for bead in positive_bead:
        stronger_eplet_on_bead[bead] = set()
        strong_eplet_on_bead[bead] = set()

    for linked in link_between_pos:
        bead1 = linked.split(" ")[0]
        bead2 = linked.split(" ")[1]

        for eplet in always_present_eplet:
            if (eplet in always_present_eplet_dict[bead1]) & (eplet in always_present_eplet_dict[bead2]):
                stronger_eplet_on_link[linked].append(eplet)
            elif eplet in always_present_eplet_dict[bead1] :
                stronger_eplet_on_bead[bead1].add(eplet)
            elif eplet in always_present_eplet_dict[bead2]:
                stronger_eplet_on_bead[bead2].add(eplet)

        for eplet in not_always_present_eplet:
            if (eplet in not_always_present_eplet_dict[bead1]) & (eplet in not_always_present_eplet_dict[bead2]):
                strong_eplet_on_link[linked].append(eplet)
            elif eplet in not_always_present_eplet_dict[bead1] :
                strong_eplet_on_bead[bead1].add(eplet)
            elif eplet in not_always_present_eplet_dict[bead2]:
                strong_eplet_on_bead[bead2].add(eplet)

    for not_linked in positive_not_linked:
        for eplet in always_present_eplet:
            stronger_eplet_on_bead[not_linked].add(eplet)

        for eplet in not_always_present_eplet:
            if eplet in not_always_present_eplet_dict[not_linked]:
                strong_eplet_on_bead[not_linked].add(eplet)

    return stronger_eplet_on_link, strong_eplet_on_link, stronger_eplet_on_bead, strong_eplet_on_bead


def A_or_B_eplet(path_to_DQ_or_DP):
    df_A_B = pd.read_csv(path_to_DQ_or_DP).set_index("allele")

    eplet_from_A = set()
    eplet_from_B = set()

    for i in df_A_B.index:
        for eplet in list(df_A_B.loc[i]):
            if type(eplet) == str:
                if "A1" in i:
                    eplet_from_A.add(eplet.replace(" ",""))
                if "B1" in i :
                    eplet_from_B.add(eplet.replace(" ",""))

    return eplet_from_A, eplet_from_B

def set_off_all_written_eplet(stronger_eplet_on_link, strong_eplet_on_link, stronger_eplet_on_bead, strong_eplet_on_bead):
    all_written_stronger = set()
    all_written_strong = set()

    for j in stronger_eplet_on_link.values():
        for eplet in j:
            all_written_stronger.add(eplet)

    for j in stronger_eplet_on_bead.values():
        for eplet in j:
            all_written_stronger.add(eplet)

    for j in strong_eplet_on_link.values():
        for eplet in j:
            all_written_strong.add(eplet)

    for j in strong_eplet_on_bead.values():
        for eplet in j:
            all_written_strong.add(eplet)

    return all_written_stronger, all_written_strong

def reorder_dict_by_eplet_frequency(eplet_dict):
    frequency_count = {}

    for beads, eplets in eplet_dict.items():
        for eplet in eplets:
            if eplet not in frequency_count.keys():
                frequency_count[eplet] = 1
            else :
                frequency_count[eplet] += 1

    frequency_count = {k: v for k, v in sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)}

    new_eplet_dict = {}

    for beads, eplets in eplet_dict.items():
        new_eplets_list = []
        for i,j in frequency_count.items():
            if i in eplets:
                new_eplets_list.append(i)

        new_eplet_dict[beads] = new_eplets_list

    return new_eplet_dict