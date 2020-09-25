import write_svg
import eplet_extraction
import write_eplet


def write_whole_svg(
        template_graph, mfi, edges, eplet_path, output, allele_type, cutoff
):
    # Make list from each line of the template
    svg_list = [i for i in open(template_graph, "r")]

    # add blank font in the list, on 20th line
    svg_list.insert(
        20,
        """ <rect  x="-2000" y="-2000" width="10000%" height="1000000%" fill="white" />""",
    )

    # extrait les indices des lignes des noeuds, edges et texte.
    # NEED ?
    # edges_ligne, circle_ligne, text_ligne = write_svg.get_edges_dictionnary(svg_liste)

    data = write_svg.parse_excel_file(mfi)
    edges_ligne = write_svg.get_edges_dictionnary(svg_list)[0]

    # Create liste of link between positive beads
    link_between_pos = write_svg.find_link_between_pos(data, edges, cutoff)

    # Create liste of positive bead, ambiguous bead, negative bead
    positive_bead, ambiguous_bead, negative_bead = eplet_extraction.get_beads_statut(data, cutoff, allele_type)

    # Update svg_liste by coloring positive edges
    # WARNING : Check stability
    svg_list = write_svg.replace_edges_color(
        svg_list, edges_ligne, link_between_pos
    )
    # Liste of positive nodes, ambiguous nodes. Each node is list with node_id, line of opacity and line of color
    node_to_color, node_to_color_light = write_svg.node_color_to_change_v2(svg_list, data, cutoff)
    ratio = write_svg.opacity_intensity(data)

    # Update svg_liste by coloring positive nodes
    svg_list = write_svg.replace_nodes_color_2(svg_list, node_to_color, ratio)
    svg_list = write_svg.replace_nodes_color_2_light(svg_list, node_to_color_light)

    df_eplet_file = eplet_extraction.parse_eplet_file(eplet_path)

    # Create dictionnary with couple of bead/eplets which are present on positive bead but not on negative beads
    always_present_eplet, not_always_present_eplet, always_present_eplet_dict, not_always_present_eplet_dict = eplet_extraction.get_bead_and_eplet_to_write(
        positive_bead, negative_bead, df_eplet_file)

    positive_not_linked = eplet_extraction.get_positive_but_not_linked(link_between_pos,positive_bead)

    # Create dictionnary with eplets to write on link, and eplets to write on beads.
    stronger_eplet_on_link, strong_eplet_on_link, stronger_eplet_on_bead, strong_eplet_on_bead = eplet_extraction.where_to_write_eplets(
        link_between_pos, always_present_eplet, not_always_present_eplet, always_present_eplet_dict,
        not_always_present_eplet_dict, positive_bead, positive_not_linked)


    # Get path_position and bead_position
    path_position = write_svg.get_path_position(svg_list, link_between_pos)[0]
    bead_position = write_svg.get_bead_position(svg_list)

    # Write stronger eplet on path
    svg_list = write_eplet.write_stronger_eplet_on_link(svg_list, path_position, stronger_eplet_on_link)

    # Write strong eplet on path
    svg_list = write_eplet.write_strong_eplet_on_link(svg_list, path_position, strong_eplet_on_link)

    # Write stronger eplet on bead
    svg_list = write_eplet.write_stronger_eplet_on_bead(svg_list, bead_position, stronger_eplet_on_bead, stronger_eplet_on_link)

    # Write strong eplet on bead
    svg_list = write_eplet.write_strong_eplet_on_bead(svg_list, bead_position, strong_eplet_on_bead, strong_eplet_on_link)

    write_svg.write_svg_file(svg_list, "{}.svg".format(output))
