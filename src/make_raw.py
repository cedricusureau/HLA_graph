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

def write_all_raw_data(all_raw_data):
    file = open("raw_test.csv","w")
    for allele, raw_data in all_raw_data:
        stronger = raw_data[0]
        strong = raw_data[1]
        file.write("Eplets from HLA-{} beads. These eplets are present on each positive bead \n".format(allele))
        for i,j in stronger.items():
            file.write(str(i)+",")
            for eplet in j:
                file.write(eplet+",")
            file.write("\n")

        file.write("Eplets from HLA-{} beads. These eplets are present on some of the positive bead \n".format(allele))
        for i,j in strong.items():
            file.write(i+",")
            for eplet in j:
                file.write(eplet+",")
            file.write("\n")

    file.close()


