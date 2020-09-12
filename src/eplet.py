import pandas as pd


def get_eplet_from_positive_beads(data, eplet_path):

    eplet = pd.read_csv(eplet_path)
    eplet = eplet.set_index("allele")
    positive_bead = []
    for i, j in data.items():
        if "A" in i:
            if j > 2000:
                positive_bead.append(i)

    eplet_from_positive_beads = {}
    for i in positive_bead:

        eplet_from_positive_beads[i] = list(eplet.loc[i])

    return eplet_from_positive_beads


def find_most_common_eplets(eplet_from_positive_beads):
    eplet_set = set()
    for i in eplet_from_positive_beads.values():
        for j in i:
            if type(j) == str:
                eplet_set.add(j.replace(" ",""))

    eplet_count_dict = {}
    for eplet in list(eplet_set):
        eplet_count_dict[eplet] = 0

    for eplet_list in eplet_from_positive_beads.values():
        for eplet in eplet_list:
            if type(eplet) == str:
                eplet_count_dict[eplet.replace(" ","")]+=1

    eplet_ratio_dict = {}
    for i,j in eplet_count_dict.items():
        eplet_ratio_dict[i] = j/len(eplet_from_positive_beads.keys())

    return {k: v for k, v in sorted(eplet_ratio_dict.items(),reverse=True, key=lambda item: item[1])}