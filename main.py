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
    default="data/graph_template/HLA_B_test.svg",
)
parser.add_argument(
    "-ep",
    "--eplet",
    help="Insert eplet file",
    type=str,
    default="data/eplets/B.csv",
)
parser.add_argument(
    "-e",
    "--edges",
    help="Insert edges file",
    type=str,
    default="data/edges/strongly_correlated_HLA_B.csv",
)
parser.add_argument(
    "-o", "--output", help="output_prefix", type=str, default="result/test/test"
)
parser.add_argument("-c", "--cutoff", help="cutoff", type=int, default=2000)

args = parser.parse_args()

# for i in os.listdir("data/sample_example"):
#    allele_type.write_svg_for_allele(args.template,"data/sample_example/{}".format(i),args.edges,args.eplet,args.output+str(i),"A", args.cutoff)

allele_type.write_svg_for_allele(
    "data/graph_template/HLA_B_test.svg",
    "data/sample_example/SA1_ex2.xls",
    args.edges,
    args.eplet,
    args.output,
    "B",
    args.cutoff,
)

# allele_type.write_svg_for_allele(args.template,"data/sample_example/SA1_ex1.xls",args.edges, args.eplet, args.output,"B",args.cutoff)
