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
