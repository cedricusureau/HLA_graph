# -*- coding: utf-8 -*-
"""
main.py
============================
The core file of my example project
"""

import src.final_fonction as final_fonction
import argparse
import os
import src.make_raw as make_raw

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
    "-o", "--output", help="output_prefix", type=str, default="result/graph/"
)
parser.add_argument(
    "-r", "--raw", help="output_prefix", type=str, default="result/raw_data/"
)
parser.add_argument("-c", "--cutoff", help="cutoff", type=int, default=2000)
parser.add_argument("-g", "--gene", type=str, default="A B C DR DQ DP")
parser.add_argument("-qp", "--dqdp", type=str, default="data/eplets/")

args = parser.parse_args()


for mfi in os.listdir("data/sample_example/SA1/"):
    full_name_SA1="data/sample_example/SA1/{}".format(mfi)
    all_raw_data = []
    for i in ["A","B","C"]:
        if (i == "A") & ("A" in args.gene):
            a_ep = final_fonction.write_whole_svg(
                args.template+i+".svg",
                full_name_SA1,
                args.edges+i+".csv",
                args.eplet+i+".csv",
                args.output + mfi.split(".")[0] +"_"+ i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                38,
                [120,30]
                )
            all_raw_data.append(["A",make_raw.make_raw_data(a_ep)])

        if (i == "B") & ("B" in args.gene):
            b_ep = final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA1,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                args.output + mfi.split(".")[0] +"_" + i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [110, 20]
            )
            all_raw_data.append(["B", make_raw.make_raw_data(b_ep)])
        if (i == "C") & ("C" in args.gene):
            c_ep = final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA1,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                args.output + mfi.split(".")[0] +"_" + i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [120, 30]
            )
            all_raw_data.append(["C",make_raw.make_raw_data(c_ep)])

    make_raw.write_all_raw_data(all_raw_data, args.raw+mfi.split(".")[0] +"_SA1")



for mfi in os.listdir("data/sample_example/SA2/"):
    full_name_SA2="data/sample_example/SA2/{}".format(mfi)
    all_raw_data = []
    for i in ["DR","DQ","DP"]:
        if (i == "DR") & ("DR" in args.gene):
            dr_ep = final_fonction.write_whole_svg(
                args.template+i+".svg",
                full_name_SA2,
                args.edges+i+".csv",
                args.eplet+i+".csv",
                args.output + mfi.split(".")[0] +"_"+ i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                36,
                [110,35]
            )
            all_raw_data.append(["DR", make_raw.make_raw_data(dr_ep)])

        if (i == "DQ") & ("DQ" in args.gene):
            dq_ep = final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA2,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                args.output + mfi.split(".")[0] +"_"+ i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                44,
                [120, 55]
            )
            all_raw_data.append(["DQ", make_raw.make_raw_data(dq_ep)])

        if (i == "DP") & ("DP" in args.gene):
            dp_ep = final_fonction.write_whole_svg(
                args.template + i + ".svg",
                full_name_SA2,
                args.edges + i + ".csv",
                args.eplet + i + ".csv",
                args.output + mfi.split(".")[0] +"_"+ i,
                i,
                args.cutoff,
                args.dqdp + i + "_eplets.csv",
                38,
                [120, 45]
            )
            all_raw_data.append(["DP", make_raw.make_raw_data(dp_ep)])

    make_raw.write_all_raw_data(all_raw_data,args.raw+mfi.split(".")[0]+"_SA2")