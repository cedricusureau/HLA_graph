# -*- coding: utf-8 -*-
"""
main.py
============================
The core file of my example project
"""

import final_fonction
import argparse
import os
import make_raw

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
parser.add_argument("-g", "--gene", type=str, default="A B C DR DQ DP")
parser.add_argument("-qp", "--dqdp", type=str, default="data/eplets/")

args = parser.parse_args()


for mfi in os.listdir("data/sample_example/SA1/"):
    full_name_SA1="data/sample_example/SA1/{}".format(mfi)
    for i in ["A","B","C"]:
        if (i == "A") & ("A" in args.gene):
            a_ep = final_fonction.write_whole_svg(
                args.template+i+".svg",
                full_name_SA1,
                args.edges+i+".csv",
                args.eplet+i+".csv",
                "result/test/"+mfi+i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [110,20]
                )
        if (i == "B") & ("B" in args.gene):
            b_ep = final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA1,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                "result/test/" + mfi + i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [110, 20]
            )
        if (i == "C") & ("C" in args.gene):
            c_ep = final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA1,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                "result/test/" + mfi + i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [110, 20]
            )
    all_raw_data = [["A",make_raw.make_raw_data(a_ep)], ["B", make_raw.make_raw_data(b_ep)], ["C", make_raw.make_raw_data(c_ep)]]
    make_raw.write_all_raw_data(all_raw_data)



for mfi in os.listdir("data/sample_example/SA2/"):
    full_name_SA2="data/sample_example/SA2/{}".format(mfi)
    for i in ["DR","DQ","DP"]:
        if (i == "DR") & ("DR" in args.gene):
            final_fonction.write_whole_svg(
                args.template+i+".svg",
                full_name_SA2,
                args.edges+i+".csv",
                args.eplet+i+".csv",
                "result/test/"+mfi+i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [90,30]
            )
        if (i == "DQ") & ("DQ" in args.gene):
            final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA2,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                "result/test/" + mfi + i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [90, 30]
            )
        if (i == "DP") & ("DP" in args.gene):
            final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA2,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                "result/test/" + mfi + i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [90, 30]
            )

