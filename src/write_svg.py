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
        if bool_to_change[i] == True:
            color_ligne_to_change.append(circle_ligne[i] + 7)

    return color_ligne_to_change


def rewrite_svg_file(svg, to_color, output):
    file1 = open(output, "w")
    for i, j in enumerate(svg):
        if i in to_color:
            file1.write(j.replace("#000000", "#FF0000"))
        elif i + 1 in to_color:
            file1.write(j.replace('fill-opacity="0.2"', 'fill-opacity="0.4"'))
        else:
            file1.write(j)
    file1.close()
