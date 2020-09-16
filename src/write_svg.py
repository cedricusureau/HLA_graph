import pandas as pd

def get_bead_position(svg_liste):
    bead_position = {}

    for indice, ligne in enumerate(svg_liste):
        if "<circle" in ligne:
            tmp_xy = []
            for i, j in enumerate(svg_liste[indice:]):
                if "cx" in j :
                    tmp_xy.append(j.replace('       cx="',"").replace('"\n',""))
                if "class" in j:
                    tmp_bead = j.split("class=")[1].split('"')[1].replace("id_","")
                if "cy" in j :
                    tmp_xy.append(j.replace('       cy="', "").replace('"\n', ""))

                if len(tmp_xy) == 2 :
                    bead_position[tmp_bead] = tmp_xy
                    break
    return bead_position


def get_edges_dictionnary(svg_liste):
    edges_ligne = {}
    circle_ligne = {}
    text_ligne = {}

    for indice, ligne in enumerate(svg_liste):
        if "<path" in ligne:
            for i,j in enumerate(svg_liste[indice:]):
                if "class" in j :
                    edges_ligne[svg_liste[indice + i].split("class=")[1].split('"')[1]] = (
                        int(indice) + i
                    )

        if "<circle" in ligne:
            for i,j in enumerate(svg_liste[indice:]):
                if "class" in j :
                    circle_ligne[svg_liste[indice + i].split("class=")[1].split('"')[1]] = (
                        int(indice) + i
                    )

        if "<text" in ligne:
            for i, j in enumerate(svg_liste[indice:]):
                if "class" in j:
                    text_ligne[svg_liste[indice + i].split("class=")[1].split('"')[1]] = (
                        int(indice) + i
                    )
    return edges_ligne, circle_ligne, text_ligne


def parse_excel_file(excel_path):
    df = pd.read_excel(excel_path)
    dico = {}
    for i in df.index:
        dico[df[df.columns[0]][i]] = df[df.columns[1]][i]
    return dico


def node_color_to_change(circle_ligne, MFI,cutoff):

    clé = []
    for i in circle_ligne.keys():
        clé.append(i.replace("_id",""))

    bool_to_change = {}

    for i in clé:
        bool_to_change[i.replace("_id","")] = False

    for i, j in MFI.items():
        if j > cutoff:
            bool_to_change[i.replace("id_","")] = True

    color_ligne_to_change = []
    for i in circle_ligne.keys():
        if bool_to_change[i] == True:
            color_ligne_to_change.append(circle_ligne[i])
    print(color_ligne_to_change)
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


def find_link_between_pos(MFI_value, edge_file,cutoff):

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

        if ident.replace("id_", "") in link_between_pos:

            new_svg[i + 2] = svg[i + 2].replace("#000000", "#FF0000")
            new_svg[i - 2] = svg[i - 2].replace("1.0", "3.0")

    return new_svg

def get_middle_position_between_positive_beads(svg, link_between_pos, bead_position):
    circle_position = {}
    linked_positive_beads = set()

    for i in link_between_pos:
        tmp_bead1=i.split(" ")[0]
        tmp_bead2=i.split(" ")[1]

        linked_positive_beads.add(tmp_bead1)
        linked_positive_beads.add(tmp_bead2)

    middle_link_pos = {}

    for i in link_between_pos:
        tmp_x = (float(bead_position[i.split(" ")[0]][0]) + float(bead_position[i.split(" ")[1]][0]))/2
        tmp_y = (float(bead_position[i.split(" ")[0]][1]) + float(bead_position[i.split(" ")[1]][1]))/2

        middle_link_pos[i] = [tmp_x, tmp_y]

    return middle_link_pos


def write_text_on_svg(svg,x,y,font_size=24, font_family="Dialog",color="#FA8072", text="test"):

    template_liste=[]
    template_liste.append('    <text\n')
    template_liste.append('       font-size="24"\n')
    template_liste.append('       x="{}"\n'.format(x))
    template_liste.append('       y="{}"\n'.format(y))
    template_liste.append('       style="font-size:{}px;font-family:{};dominant-baseline:central;text-anchor:middle;fill:{}"\n'.format(font_size, font_family,color))
    template_liste.append('       class="eplet"\n')
    template_liste.append('       id="text218">{}</text>"""\n'.format(text))

    for i in template_liste:
        svg.insert(-2,i)
    return svg


def write_1_ratio_eplet(svg, ratio, middle_position_between_positive_beads):

    for eplet,score in ratio.items():
        if score == 1:

            for position in middle_position_between_positive_beads.values():
                svg = write_text_on_svg(svg, position[0], position[1]-10, font_size=18, font_family="Dialog",color="#8B0000", text=eplet)

    return svg

def write_class_2_eplet(svg, link_for_second_class_eplets, middle_position_between_positive_beads):
    already_write = []
    for j in link_for_second_class_eplets.values():
        already_write = [1 for k in range(len(j))]

    for eplet, booleen in link_for_second_class_eplets.items():
        count = -1
        for i in booleen:
            count += 1
            if i[1] == True:
                tmp_pos=middle_position_between_positive_beads[i[0]]
                svg = write_text_on_svg(svg,tmp_pos[0],tmp_pos[1]+(15*already_write[count])-8, font_size=12,font_family="Dialog",color="#4682B4", text=eplet)
                already_write[count] += 1
    return svg

def get_position_of_beads(svg, beads_liste, bead_position):
    position_of_beads = {}
    for i in beads_liste:
        position_of_beads[i] = [float(k) for k in bead_position[i]]

    return position_of_beads

def write_3_class_eplet(svg, eplets_on_isolated_beads, isolated_bead, position_of_isolated_beads, eplet_path):
    eplet_data = pd.read_csv(eplet_path)
    eplet_data = eplet_data.set_index("allele")
    already_write = {}
    for bead in isolated_bead:
        already_write[bead] = 1

    for eplet in eplets_on_isolated_beads:
        for bead in isolated_bead:
            if eplet in list(eplet_data.loc[bead]):
                svg = write_text_on_svg(svg,position_of_isolated_beads[bead][0]+30, position_of_isolated_beads[bead][1]-60+(15*already_write[bead]), font_size=12,font_family="Dialog",color="#FFA500", text=eplet)
                already_write[bead] += 1
    return svg