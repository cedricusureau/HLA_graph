# -*- coding: utf-8 -*-
"""
main.py
============================
The core file of my example project
"""

import argparse
import os

import allele_type

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

args = parser.parse_args()


for mfi in os.listdir("data/sample_example/patients"):
    full_name="data/sample_example/patients/{}".format(mfi)
    for i in ["A","B","C"]:
        allele_type.write_svg_for_allele(
            args.template+i+".svg",
            full_name,
            args.edges+i+".csv",
            args.eplet+i+".csv",
            full_name+i,
            i,
            args.cutoff,
        )

# allele_type.write_svg_for_allele(args.template,"data/sample_example/SA1_ex1.xls",args.edges, args.eplet, args.output,"B",args.cutoff)
