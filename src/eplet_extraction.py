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
    return positive_beads, ambiguous_bead, negative_bead

def get_bead_and_eplet_to_write(positive_bead, negative_bead, df_eplet_file):
    eplet_carried_by_negative_bead = []

    for bead in negative_bead:
        for eplet in get_eplets_list_from_beads(bead,df_eplet_file):
            eplet_carried_by_negative_bead.append(eplet)

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

def where_to_write_eplets(link_between_pos, always_present_eplet, not_always_present_eplet, always_present_eplet_dict, not_always_present_eplet_dict, positive_bead):
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

    return stronger_eplet_on_link, strong_eplet_on_link, stronger_eplet_on_bead, strong_eplet_on_bead