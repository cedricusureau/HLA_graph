import pandas as pd


def get_eplet_from_beads(data, eplet_path, allele_type, cutoff):

    eplet = pd.read_csv(eplet_path)
    eplet = eplet.set_index("allele")
    positive_bead = []
    negative_bead = []
    for i, j in data.items():
        if allele_type in i:
            if j > cutoff:
                positive_bead.append(i)
    for i, j in data.items():
        if allele_type in i:
            if j < cutoff:
                negative_bead.append(i)

    eplet_from_positive_beads = {}
    eplet_from_negative_beads = {}
    for i in positive_bead:
        eplet_from_positive_beads[i] = list(eplet.loc[i])

    for i in negative_bead:
        eplet_from_negative_beads[i] = list(eplet.loc[i])

    return eplet_from_positive_beads, eplet_from_negative_beads

def find_most_common_eplets(eplet_from_beads):
    eplet_set = set()
    for i in eplet_from_beads.values():
        for j in i:
            if type(j) == str:
                eplet_set.add(j)

    eplet_count_dict = {}
    for eplet in list(eplet_set):
        eplet_count_dict[eplet] = 0

    for eplet_list in eplet_from_beads.values():
        for eplet in eplet_list:
            if type(eplet) == str:
                 eplet_count_dict[eplet]+=1

    eplet_ratio_dict = {}
    for i,j in eplet_count_dict.items():
        eplet_ratio_dict[i] = j/len(eplet_from_beads.keys())

    return {k: v for k, v in sorted(eplet_ratio_dict.items(),reverse=True, key=lambda item: item[1])}

def compare_ratio(pos_eplet_ratio_dict, neg_eplet_ratio_dict):
    pos_neg_ratio = {}
    for i,j in pos_eplet_ratio_dict.items():
        if i in neg_eplet_ratio_dict.keys():
            pos_neg_ratio[i] = pos_eplet_ratio_dict[i]-neg_eplet_ratio_dict[i]
        else :
            pos_neg_ratio[i] = j

    return {k: v for k, v in sorted(pos_neg_ratio.items(),reverse=True, key=lambda item: item[1])}

def get_second_class_eplet(pos_eplet_ratio_dict, neg_eplet_ratio_dict):
    second_class_eplet = {}
    for i,j in pos_eplet_ratio_dict.items():
        if (j > 0.5) & (j!=1)&(i not in neg_eplet_ratio_dict.keys()):
            second_class_eplet[i] = j

    return second_class_eplet

def get_link_for_second_class_eplets(link_between_pos, eplet_path, second_class_eplet):
    eplet_data = pd.read_csv(eplet_path)
    eplet_data = eplet_data.set_index("allele")
    link_to_write = {}

    for eplet in second_class_eplet:
        link_to_write[eplet] = []
        for i in link_between_pos:
            allele1 = i.split(' ')[0]
            allele2 = i.split(' ')[1]

            compo1 = [i.replace(" ","") for i in list(eplet_data.loc[allele1]) if type(i)==str]
            compo2 = [i.replace(" ","") for i in list(eplet_data.loc[allele2]) if type(i)==str]

            if (eplet in compo1) & (eplet in compo2):
                link_to_write[eplet].append([i,True])
            else :
                link_to_write[eplet].append([i,False])
    return link_to_write

def get_eplets_on_isolated_beads(ratio, second_class_eplet):
    eplets_on_isolated_beads=[]

    for i,j in ratio.items():
        if j == 1:
            eplets_on_isolated_beads.append(i)

    for i in second_class_eplet:
        eplets_on_isolated_beads.append(i)

    return eplets_on_isolated_beads

def get_isolated_beads(MFI, link_between_pos, allele_type):
    linked_pos = set()

    for i in link_between_pos:
        linked_pos.add(i.split(" ")[0])
        linked_pos.add(i.split(" ")[1])

    isolated_beads = []
    for i,j in MFI.items():
        if allele_type in i:
            if j > 2000:
                if i not in linked_pos:
                    isolated_beads.append(i)
    return isolated_beads