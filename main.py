# -*- coding: utf-8 -*-
"""
main.py
============================
The core file of my example project
"""

import argparse

import write_svg

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "-d",
    "--mfi",
    type=str,
    help="Insert MFI file value (.xls)",
    default="data/sample_example/SA1_ex1.xls",
)
parser.add_argument(
    "-t",
    "--template",
    help="Insert template file",
    type=str,
    default="data/graph_template/HLA_A_V2.svg",
)
parser.add_argument(
    "-e",
    "--edges",
    help="Insert edges file",
    type=str,
    default="data/edges/strongly_correlated_HLA_A.csv",
)
parser.add_argument(
    "-o", "--output", help="output_prefix", type=str, default="result/test/test.svg"
)

args = parser.parse_args()

svg_liste = [i for i in open(args.template, "r")]

edges_ligne, circle_ligne, text_ligne = write_svg.get_edges_dictionnary(svg_liste)
data = write_svg.parse_excel_file(args.mfi)
link_between_pos = write_svg.find_link_between_pos(data, args.edges)

edges_colored_svg = write_svg.replace_edges_color(
    svg_liste, edges_ligne, link_between_pos
)


node_to_color = write_svg.node_color_to_change(circle_ligne, data)
print(node_to_color)

node_edges_colored_svg = write_svg.replace_nodes_color(edges_colored_svg, node_to_color)

write_svg.write_svg_file(node_edges_colored_svg, args.output)
