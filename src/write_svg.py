import pandas as pd


def get_bead_position(svg_liste):
    bead_position = {}

    for indice, ligne in enumerate(svg_liste):
        if "<circle" in ligne:
            tmp_xy = []
            for i, j in enumerate(svg_liste[indice:]):
                if "cx" in j:
                    tmp_xy.append(float(j.replace('       cx="', "").replace('"\n', "")))
                if "class" in j:
                    tmp_bead = j.split("class=")[1].split('"')[1].replace("id_", "").replace(",__", "")
                if "cy" in j:
                    tmp_xy.append(float(j.replace('       cy="', "").replace('"\n', "")))

                if len(tmp_xy) == 2:
                    bead_position[tmp_bead] = tmp_xy
                    break

    return bead_position


def get_edges_dictionnary(svg_liste):
    edges_ligne = {}
    circle_ligne = {}
    text_ligne = {}

    for indice, ligne in enumerate(svg_liste):
        if "<path" in ligne:
            for i, j in enumerate(svg_liste[indice:]):
                if "class" in j:
                    edges_ligne[
                        svg_liste[indice + i].split("class=")[1].split('"')[1]
                    ] = (int(indice) + i)
                    break

        if "<circle" in ligne:
            for i, j in enumerate(svg_liste[indice:]):
                if "class" in j:
                    circle_ligne[
                        svg_liste[indice + i].split("class=")[1].split('"')[1]
                    ] = (int(indice) + i)
                    break
        if "<text" in ligne:
            for i, j in enumerate(svg_liste[indice:]):
                if "class" in j:
                    text_ligne[
                        svg_liste[indice + i].split("class=")[1].split('"')[1]
                    ] = (int(indice) + i)
                    break
    return edges_ligne, circle_ligne, text_ligne

def opacity_intensity(data):
    ratio = {}
    for bead, value in data.items():
        if value/10000 > 1:
            ratio[bead] = 0.8
        else :
           ratio[bead] = value/10000
    return ratio


def parse_excel_file(excel_path):
    df = pd.read_excel(excel_path)
    dico = {}
    for i in df.index:
        allele_name = df[df.columns[0]][i]
        if "DP" in allele_name:
            allele_name = allele_name[:10] + ", " + allele_name[10:]

        dico[df[df.columns[0]][i]] = df[df.columns[1]][i]

    return dico


def node_color_to_change_v2(svg_liste, MFI, cutoff):
    to_color = []
    to_color_light = []
    to_delete = []

    for indice, ligne in enumerate(svg_liste):
        if "<circle" in ligne:
            tmp_fill_ligne = 0
            tmp_fill_opacity_ligne = 0
            for i, j in enumerate(svg_liste[indice:]):
                if "fill=" in j:
                    tmp_fill_ligne = indice + i
                if "fill-opacity" in j:
                    tmp_fill_opacity_ligne = indice + i
                if "class=" in j:
                    tmp_id = (
                        j.replace('class="id_', "")
                            .replace('"', "")
                            .replace("       ", "")
                            .replace("\n", "")
                            .replace(",__", "")
                    )

                    if tmp_id in MFI.keys():

                        if MFI[tmp_id] > cutoff:
                            to_color.append(
                                [tmp_id, tmp_fill_ligne, tmp_fill_opacity_ligne]
                            )

                    if tmp_id in MFI.keys():

                        if (MFI[tmp_id] < cutoff) & (MFI[tmp_id] > 1000):
                            to_color_light.append(
                                [tmp_id, tmp_fill_ligne, tmp_fill_opacity_ligne]
                            )

                        if MFI[tmp_id] < 1000:
                            to_delete.append(
                                [tmp_id, tmp_fill_ligne, tmp_fill_opacity_ligne]
                            )
                    break
    return to_color, to_color_light, to_delete


def write_svg_file(svg, output):
    file1 = open(output, "w")
    for ligne in svg:
        file1.write(ligne)
    file1.close()


def replace_nodes_color_2(svg, to_color, ratio):

    new_svg = svg
    for i in to_color:
        new_svg[i[1]] = new_svg[i[1]].replace("#858283", "#f15a73")
        new_svg[i[1]] = new_svg[i[1]].replace("#000000", "#f15a73")
        new_svg[i[2]] = new_svg[i[2]].replace('fill-opacity="0.2"', 'fill-opacity="{}"'.format(ratio[i[0]]))

    return new_svg


def replace_nodes_color_2_light(svg, to_color):
    new_svg = svg

    for i in to_color:
        new_svg[i[1]] = new_svg[i[1]].replace(new_svg[i[1]], '       fill="#0000ff"\n')
    return new_svg

def delete_nodes(svg, to_delete):
    new_svg = svg
    for i in to_delete:
        new_svg[i[2]] = new_svg[i[2]].replace('fill-opacity="0.2"', 'fill-opacity="0"')
    return new_svg


def find_link_between_pos(MFI_value, edge_file, cutoff):
    link_list = pd.read_csv(edge_file)
    pos_MFI_value = {}
    for i, j in MFI_value.items():
        if j > cutoff:
            pos_MFI_value[i] = j
    link_between_pos = []

    for pos in pos_MFI_value.keys():
        for source, target in zip(link_list["Source"], link_list["Target"]):
            if source == pos:
                if target in pos_MFI_value.keys():
                    link_between_pos.append(source + " " + target)

    return link_between_pos


def replace_edges_color(svg, edges_ligne, link_between_pos):
    new_svg = svg
    for ident, i in edges_ligne.items():

        if ident.replace("id_", "").replace(",__", "") in link_between_pos:
            new_svg[i + 2] = svg[i + 2].replace("#000000", "#FF0000")
            new_svg[i - 2] = svg[i - 2].replace(str(new_svg[i-2]),'       stroke-width="4"\n')
            new_svg[i + 1] = svg[i + 1].replace(str(new_svg[i+1]),'       stroke-opacity="0.2"\n')
        else :
            new_svg[i + 1] = svg[i+1].replace(str(new_svg[i+1]),'       stroke-opacity="0"\n')


    return new_svg

def write_text_on_svg(
        svg, x, y, font_size=24, font_family="Dialog", color="#FA8072", text="test"
):
    template_liste = []
    template_liste.append("    <text\n")
    template_liste.append('       font-size="24"\n')
    template_liste.append('       x="{}"\n'.format(x))
    template_liste.append('       y="{}"\n'.format(y))
    template_liste.append(
        '       style="font-size:{}px;font-family:{};dominant-baseline:central;text-anchor:middle;fill:{}"\n'.format(
            font_size, font_family, color
        )
    )
    template_liste.append('       class="eplet"\n')
    template_liste.append('       id="text218">{}</text>"""\n'.format(text))

    for i in template_liste:
        svg.insert(-2, i)
    return svg



def get_position_of_beads(svg, beads_liste, bead_position):
    position_of_beads = {}
    for i in beads_liste:
        position_of_beads[i] = [float(k) for k in bead_position[i]]

    return position_of_beads


def get_path_position_curved(svg, link_between_pos):
    path_position = {}

    for indice, ligne in enumerate(svg):
        if "<path" in ligne:
            tmp_class = ""
            tmp_pos = ""
            final_pos = ""
            for i, j in enumerate(svg[indice:]):
                if "class" in j:
                    tmp_class = j.replace("       class=", "").replace('"id_', "").replace('"\n', "").replace("id_",
                                                                                                              "").replace(
                        ",__", "")
                if "d=" in j:
                    tmp_pos = j.replace('       d="', "").split(" ")[0:5]

                    start_x = float(tmp_pos[1].split(",")[0])
                    start_y = float(tmp_pos[1].split(",")[1])

                    tmp_x1, tmp_x2 = float(tmp_pos[-2].split(",")[0]), float(tmp_pos[-1].split(",")[0])
                    tmp_y1, tmp_y2 = float(tmp_pos[-2].split(",")[1]), float(tmp_pos[-1].split(",")[1])

                    if tmp_pos[0] == "m":
                        final_pos = [start_x + (tmp_x1 + tmp_x2) / 2, start_y + (tmp_y1 + tmp_y2) / 2]

                    if tmp_pos[0] == "M":
                        final_pos = [(tmp_x1 + tmp_x2) / 2, (tmp_y1 + tmp_y2) / 2]

                if (tmp_class != "") & (tmp_pos != "") & (final_pos != ""):
                    path_position[tmp_class] = final_pos

                    break

    path_position_2 = {}

    for i, j in path_position.items():
        path_position_2[i] = j
        path_position_2[i.split(" ")[1] + " " + i.split(" ")[0]] = j

    path_position_pos = {}

    for i, j in path_position_2.items():
        if i in link_between_pos:
            path_position_pos[i] = path_position_2[i]

    return path_position_2, path_position_pos

# def get_middle_position_between_positive_beads(svg, link_between_pos, bead_position):
#     circle_position = {}
#     linked_positive_beads = set()
#
#     for i in link_between_pos:
#         tmp_bead1 = i.split(" ")[0]
#         tmp_bead2 = i.split(" ")[1]
#
#         linked_positive_beads.add(tmp_bead1)
#         linked_positive_beads.add(tmp_bead2)
#
#     middle_link_pos = {}
#
#     for i in link_between_pos:
#         tmp_x = (
#                         float(bead_position[i.split(" ")[0]][0])
#                         + float(bead_position[i.split(" ")[1]][0])
#                 ) / 2
#         tmp_y = (
#                         float(bead_position[i.split(" ")[0]][1])
#                         + float(bead_position[i.split(" ")[1]][1])
#                 ) / 2
#
#         middle_link_pos[i] = [tmp_x, tmp_y]
#
#         print(middle_link_pos)
#         # magouille
#         for i, j in middle_link_pos.items():
#             middle_link_pos[i.split(" ")[1] + " " + i.split(" ")[0]] = j
#
#         print(middle_link_pos)
#     return middle_link_pos

def get_path_position_straight(svg, link_between_pos, allele, bead_position, edges_ligne):
    path_position = {}

    for couple in edges_ligne.keys():
        bead1 = couple.split(" ")[0].replace("id_","").replace(",__","")
        bead2 = couple.split(" ")[1].replace("id_","").replace(",__","").replace(",__","")

        bead1_pos = bead_position[bead1]
        bead2_pos = bead_position[bead2]

        middle_pos = [(bead1_pos[0] + bead2_pos[0]) / 2, (bead1_pos[1] + bead2_pos[1]) / 2]
        path_position[str(bead1)+" "+str(bead2)] = middle_pos

    path_position_2 = {}
    for i,j in path_position.items():
        path_position_2[i] = j
        path_position_2[i.split(" ")[1]+" "+i.split(" ")[0]] = j

    return path_position_2

def get_bead_text_position(svg_liste):
    text_position = []
    for indice, ligne in enumerate(svg_liste):
        if "<text" in ligne:
            tmp_value = []
            for i, j in enumerate(svg_liste[indice:]):
                if "  x=" in j:
                    tmp_value.append(float(j.replace('       x="','').replace('"\n','')))
                if "  y=" in j:
                    tmp_value.append(float(j.replace('       y="','').replace('"\n','')))

                if len(tmp_value) == 2:
                    text_position.append(tmp_value)
                    break

    return text_position