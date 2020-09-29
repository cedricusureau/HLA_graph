# -*- coding: utf-8 -*-
"""
main.py
============================
The core file of my example project
"""

import final_fonction
import argparse
import os

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "-d",
    "--mfi",
    type=str,
    help="Insert MFI file value (.xls)",
    default="data/sample_example/SA1_ex2.xls",
)
parser.add_argument(
    "-t",
    "--template",
    help="Insert template file",
    type=str,
    default="data/graph_template/",
)
parser.add_argument(
    "-ep",
    "--eplet",
    help="Insert eplet file",
    type=str,
    default="data/eplets/",
)
parser.add_argument(
    "-e",
    "--edges",
    help="Insert edges file",
    type=str,
    default="data/edges/",
)
parser.add_argument(
    "-o", "--output", help="output_prefix", type=str, default="result/test/"
)
parser.add_argument("-c", "--cutoff", help="cutoff", type=int, default=2000)

parser.add_argument("-qp", "--dqdp", type=str, default="data/eplets/")

args = parser.parse_args()


#for mfi in os.listdir("data/sample_example/patients"):
#    full_name="data/sample_example/patients/{}".format(mfi)
#    print(full_name)
#    for i in ["A","B","C"]:
#        allele_type.write_svg_for_allele(
#            args.template+i+".svg",
#            full_name,
#            args.edges+i+".csv",
#            args.eplet+i+".csv",
#            "result/test/"+mfi+i,
#            i,
#            args.cutoff,
#        )

# for mfi in os.listdir("data/sample_example/SA2/"):
#     full_name="data/sample_example/SA2/{}".format(mfi)
#     for i in ["DP"]:
#         allele_type.write_svg_for_allele(
#             args.template+i+".svg",
#             full_name,
#             args.edges+i+".csv",
#             args.eplet+i+".csv",
#             "result/test/"+mfi+i,
#             i,
#             args.cutoff,
#         )

# for mfi in os.listdir("data/sample_example/SA2/"):
#     full_name="data/sample_example/SA2/{}".format(mfi)
#     for i in ["DQ","DP","DR"]:
#         final_fonction.write_whole_svg(
#             args.template+i+".svg",
#             full_name,
#             args.edges+i+".csv",
#             args.eplet+i+".csv",
#             "result/test/"+mfi+i,
#             i,
#             args.cutoff,
#             args.dqdp+i+"_eplets.csv"
#         )

# for mfi in os.listdir("data/sample_example/SA1/"):
#     full_name="data/sample_example/SA1/{}".format(mfi)
#     for i in ["A","B","C"]:
#         final_fonction.write_whole_svg(
#             args.template+i+".svg",
#             full_name,
#             args.edges+i+".csv",
#             args.eplet+i+".csv",
#             "result/test/"+mfi+i,
#             i,
#             args.cutoff,
#             args.dqdp + i + "_eplets.csv",
#             30
#         )

for mfi in os.listdir("data/sample_example/SA1/"):
    full_name="data/sample_example/SA1/{}".format(mfi)
    for i in ["A"]:
        final_fonction.write_whole_svg(
            args.template+i+".svg",
            full_name,
            args.edges+i+".csv",
            args.eplet+i+".csv",
            "result/test/"+mfi+i,
            i,
            args.cutoff,
            args.dqdp + i + "_eplets.csv",
            36,
            [110,20]
        )

for mfi in os.listdir("data/sample_example/SA1/"):
    full_name="data/sample_example/SA1/{}".format(mfi)
    for i in ["B"]:
        final_fonction.write_whole_svg(
            args.template+i+".svg",
            full_name,
            args.edges+i+".csv",
            args.eplet+i+".csv",
            "result/test/"+mfi+i,
            i,
            args.cutoff,
            args.dqdp + i + "_eplets.csv",
            36,
            [110,20]
        )

for mfi in os.listdir("data/sample_example/SA1/"):
    full_name="data/sample_example/SA1/{}".format(mfi)
    for i in ["C"]:
        final_fonction.write_whole_svg(
            args.template+i+".svg",
            full_name,
            args.edges+i+".csv",
            args.eplet+i+".csv",
            "result/test/"+mfi+i,
            i,
            args.cutoff,
            args.dqdp + i + "_eplets.csv",
            36,
            [110,20]
        )
#allele_type.write_svg_for_allele("data/graph_template/DP.svg", "data/sample_example/AFIR NORDINE.xls", "data/edges/strongly_correlated_HLA_DP.csv","data/eplets/DP_beads.csv","test_DP","DP",1000)
#allele_type.write_svg_for_allele(args.template,"data/sample_example/SA1_ex1.xls",args.edges, args.eplet, args.output,"B",args.cutoff)
