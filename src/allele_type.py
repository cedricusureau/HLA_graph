import eplet_management
import write_svg
from cairosvg import svg2png


def write_svg_for_allele(
    template_graph, mfi, edges, eplet, output, allele_type, cutoff
):
    # créer une liste avec toute les lignes du svg
    svg_liste = [i for i in open(template_graph, "r")]

    svg_list = svg_liste.insert(
        20,
        """ <rect  x="-2000" y="-2000" width="10000%" height="1000000%" fill="white" />""",
    )
    write_svg.get_bead_position(svg_liste)
    # extrait les indices des lignes des noeuds, edges et texte.
    edges_ligne, circle_ligne, text_ligne = write_svg.get_edges_dictionnary(svg_liste)

    # data = MFI values
    data = write_svg.parse_excel_file(mfi)

    # extrait les listes des edges entre les billes positives
    link_between_pos = write_svg.find_link_between_pos(data, edges, cutoff)

    # créer un fichier svg avec les edges coloré

    edges_colored_svg = write_svg.replace_edges_color(
        svg_liste, edges_ligne, link_between_pos
    )

    # extrait les lignes des noeuds à colorer
    node_to_color = write_svg.node_color_to_change_v2(svg_liste, data, cutoff)[0]
    node_to_color_light = write_svg.node_color_to_change_v2(svg_liste, data, cutoff)[1]

    # créer un fichier svg avec le noeuds coloré
    node_edges_colored_svg = write_svg.replace_nodes_color_2(svg_liste, node_to_color)
    node_edges_colored_svg = write_svg.replace_nodes_color_2_light(node_edges_colored_svg, node_to_color_light)
    # Pos_bead_eplet contient la liste d'eplet pos et neg
    pos_bead_eplet, neg_bead_eplet = eplet_management.get_eplet_from_beads(
        data, eplet, allele_type, cutoff
    )

    # Calcul des ratios:
    # pos_ratio = ratio des billes pos pour un eplet
    # neg_ratio = ratio des billes neg pour un eplet
    pos_eplet_ratio_dict = eplet_management.find_most_common_eplets(pos_bead_eplet)
    neg_eplet_ratio_dict = eplet_management.find_most_common_eplets(neg_bead_eplet)



    # ratio = pour chaque eplet, calcul du nombre de bille pos porteuse - nombre de bille neg porteuse
    ratio = eplet_management.compare_ratio(pos_eplet_ratio_dict, neg_eplet_ratio_dict)

    # Coordonnée x,y à mi-chemin des billes
    #middle_position_between_positive_beads = (
    #    write_svg.get_middle_position_between_positive_beads(
    #        svg_liste, link_between_pos, write_svg.get_bead_position(svg_liste)
    #    )
    #)

    middle_position_between_positive_beads = write_svg.get_path_position(svg_liste, link_between_pos)

    # écrit les eplets avec un ratio de 1
    new_svg = write_svg.write_1_ratio_eplet(
        node_edges_colored_svg, ratio, middle_position_between_positive_beads
    )

    # Génére la liste des eplets présent sur certaines billes positives mais pas les billes négatives
    second_class_eplet = eplet_management.get_second_class_eplet(
        pos_eplet_ratio_dict, neg_eplet_ratio_dict
    )
    # Vérifie les liens concerné par un partage d'éplet présent sur certaines billes positives mais pas les billes négatives


    link_for_second_class_eplets = eplet_management.get_link_for_second_class_eplets(
        link_between_pos, eplet, second_class_eplet
    )


    # Ecrit en bleu les noms des eplets concerné
    new_svg2 = write_svg.write_class_2_eplet(
        new_svg, link_for_second_class_eplets, middle_position_between_positive_beads
    )

    # Extrait tout les eplets déjà marqué
    eplets_on_isolated_beads = eplet_management.get_eplets_on_isolated_beads(
        ratio, second_class_eplet
    )

    # Extrait les billes isolées
    isolated_bead = eplet_management.get_isolated_beads(
        data, link_between_pos, allele_type, cutoff
    )

    # Extrait les positions des billes isolées
    position_of_isolated_beads = write_svg.get_position_of_beads(
        svg_liste, isolated_bead, write_svg.get_bead_position(svg_liste)
    )

    eplet_to_write_alone_bead = eplet_management.get_eplets_from_alone_pos_beads(data,link_between_pos, cutoff, pos_bead_eplet, neg_bead_eplet, allele_type)
    all_eplet_to_write_alone_bead = []
    for i in eplet_to_write_alone_bead.values():
        for j in i:
            all_eplet_to_write_alone_bead.append(j)

    # Ecrit les eplets sur les billes isolées
    new_svg3 = write_svg.write_3_class_eplet(
        new_svg2,
        eplets_on_isolated_beads,
        isolated_bead,
        position_of_isolated_beads,
        eplet,
        all_eplet_to_write_alone_bead
    )

    position_of_alone_bead = write_svg.get_position_of_beads(new_svg3, list(eplet_to_write_alone_bead.keys()), write_svg.get_bead_position(svg_liste))

    new_svg4 = write_svg.write_4_class_eplet(
        new_svg3,
        all_eplet_to_write_alone_bead,
        list(eplet_to_write_alone_bead.keys()),
        position_of_alone_bead,
        eplet,
    )

    # Génère le fichier final
    write_svg.write_svg_file(new_svg4, "{}.svg".format(output))
    #svg2png(write_to="{}.png".format(output), bytestring="".join(new_svg3))
