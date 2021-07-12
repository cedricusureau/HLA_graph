import src.write_svg as write_svg
import src.eplet_extraction as eplet_extraction
import src.write_eplet as write_eplet
import src.make_raw as make_raw


def write_whole_svg(
        template_graph, mfi, edges, eplet_path, output, allele_type, cutoff, path_to_DQ_or_DP, text_size, text_position
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
    data, unknown_allele = write_svg.clean_mfi_data(allele_type, data)
    edges_ligne = write_svg.get_edges_dictionnary(svg_list)[0]
    # Create liste of link between positive beads
    link_between_pos = write_svg.find_link_between_pos(data, edges, cutoff)

    bead_text_position = write_svg.get_bead_text_position(svg_list)

    # Create liste of positive bead, ambiguous bead, negative bead
    positive_bead, ambiguous_bead, negative_bead = eplet_extraction.get_beads_statut(data, cutoff, allele_type)

    # Update svg_liste by coloring positive edges
    # WARNING : Check stability
    svg_list = write_svg.replace_edges_color(
        svg_list, edges_ligne, link_between_pos
    )
    # Liste of positive nodes, ambiguous nodes. Each node is list with node_id, line of opacity and line of color
    node_to_color, node_to_color_light, to_delete = write_svg.node_color_to_change_v2(svg_list, data, cutoff)
    ratio = write_svg.opacity_intensity(data)

    # Update svg_liste by coloring positive nodes
    svg_list = write_svg.replace_nodes_color_2(svg_list, node_to_color, ratio)
    svg_list = write_svg.replace_nodes_color_2_light(svg_list, node_to_color_light)
    svg_list = write_svg.delete_nodes(svg_list,to_delete)

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
    bead_position = write_svg.get_bead_position(svg_list)
    path_position = write_svg.get_path_position_straight(svg_list, link_between_pos,allele_type, bead_position, edges_ligne)
    # path_position = write_svg.get_path_position_curved(svg_list, link_between_pos)[0]
    #Few reformating of eplets dictionnary. The most frequent eplets are displayed first. Check for the sens of the couple between link_position and the dictionnary too.
    strong_eplet_on_link = eplet_extraction.reorder_dict_by_eplet_frequency(strong_eplet_on_link)
    strong_eplet_on_link = write_eplet.check_couple_order(strong_eplet_on_link, path_position)

    stronger_eplet_on_link = eplet_extraction.reorder_dict_by_eplet_frequency(stronger_eplet_on_link)
    stronger_eplet_on_link = write_eplet.check_couple_order(stronger_eplet_on_link, path_position)

    strong_eplet_on_bead = eplet_extraction.reorder_dict_by_eplet_frequency(strong_eplet_on_bead)
    stronger_eplet_on_bead = eplet_extraction.reorder_dict_by_eplet_frequency(stronger_eplet_on_bead)


    # Write stronger eplet on path
    svg_list, global_written_stronger_link = write_eplet.write_stronger_eplet_on_link(svg_list, path_position, stronger_eplet_on_link, text_size, bead_text_position)


    # Write strong eplet on path
    svg_list, global_written = write_eplet.write_strong_eplet_on_link(svg_list, path_position, strong_eplet_on_link, text_size, stronger_eplet_on_link, bead_text_position, global_written_stronger_link)

    # Write stronger eplet on bead
    svg_list = write_eplet.write_stronger_eplet_on_bead(svg_list, bead_position, stronger_eplet_on_bead, stronger_eplet_on_link, text_size, text_position)

    # Write strong eplet on bead
    svg_list = write_eplet.write_strong_eplet_on_bead(svg_list, bead_position, strong_eplet_on_bead, stronger_eplet_on_bead, strong_eplet_on_link, text_size, text_position)

    if allele_type == "DQ" or allele_type == "DP":
        A_eplet, B_eplet = eplet_extraction.A_or_B_eplet(path_to_DQ_or_DP)
        all_written_stronger, all_written_strong = eplet_extraction.set_off_all_written_eplet(stronger_eplet_on_link, strong_eplet_on_link, stronger_eplet_on_bead, strong_eplet_on_bead)
        svg_list = write_eplet.write_A_or_B_eplets(svg_list, A_eplet, B_eplet, all_written_stronger, all_written_strong, allele_type)
        svg_list = write_eplet.write_A_or_B_eplets(svg_list, A_eplet, B_eplet, all_written_stronger, all_written_strong, allele_type)


    if len(mfi.split("/")) > 2:
        name =  mfi.split('/')[3]
    else :
        name =  mfi.split('/')[1]

    write_svg.write_svg_file(svg_list, "{}.svg".format(output))
    if (allele_type == "DR") or (allele_type == "A"):
        make_raw.write_json_unknown(unknown_allele, name)

    make_raw.get_forbidden_bead(df_eplet_file, stronger_eplet_on_link,stronger_eplet_on_bead, positive_bead, allele_type, name)
    json_file_name = make_raw.get_forbidden_bead_light(df_eplet_file, strong_eplet_on_link,strong_eplet_on_bead, positive_bead, allele_type, name)


    return stronger_eplet_on_link,strong_eplet_on_link,stronger_eplet_on_bead,strong_eplet_on_bead
