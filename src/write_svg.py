import pandas as pd


def get_edges_dictionnary(svg_liste):
    edges_ligne = {}
    circle_ligne = {}
    text_ligne = {}

    for indice, ligne in enumerate(svg_liste):
        if "<path" in ligne:
            edges_ligne[svg_liste[indice + 4].split("class=")[1].split('"')[1]] = (
                indice + 4
            )

        if "<circle" in ligne:
            circle_ligne[
                svg_liste[indice + 3].split("class=")[1].split('"')[1].split("id_")[1]
            ] = (indice + 3)

        if "<text" in ligne:
            text_ligne[svg_liste[indice + 5].split("class=")[1].split('"')[1]] = (
                indice + 5
            )

    return edges_ligne, circle_ligne, text_ligne


def parse_excel_file(excel_path):
    df = pd.read_excel(excel_path)
    dico = {}
    for i in df.index:
        dico[df[df.columns[0]][i]] = df[df.columns[1]][i]
    return dico


def node_color_to_change(circle_ligne, MFI):
    bool_to_change = {}

    for i in circle_ligne.keys():
        bool_to_change[i] = False

    for i, j in MFI.items():
        if j > 2000:
            bool_to_change[i] = True

    color_ligne_to_change = []

    for i in circle_ligne.keys():
        if bool_to_change[i]:
            color_ligne_to_change.append(circle_ligne[i])

    return color_ligne_to_change


def write_svg_file(svg, output):
    file1 = open(output, "w")
    for ligne in svg:
        file1.write(ligne)
    file1.close()


def replace_nodes_color(svg, to_color):
    new_svg = svg
    for i, j in enumerate(svg):
        if i in to_color:
            new_svg[i + 7] = new_svg[i + 7].replace("#000000", "#FF0000")
            new_svg[i + 3] = new_svg[i + 3].replace("#000000", "#FF0000")
        if i + 1 in to_color:
            new_svg[i + 6] = new_svg[i + 6].replace("0.2", "0.4")
            new_svg[i + 3] = new_svg[i + 3].replace(
                "fill-opacity:0.2", "fill-opacity:0.4"
            )
    return new_svg


def find_link_between_pos(MFI_value, edge_file):

    link_list = pd.read_csv(edge_file)
    pos_MFI_value = {}

    for i, j in MFI_value.items():
        if j > 2000:
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

        if ident.replace("id_", "") in link_between_pos:

            new_svg[i + 2] = svg[i + 2].replace("#000000", "#FF0000")
            new_svg[i - 2] = svg[i - 2].replace("1.0", "3.0")

    return new_svg
