# -*- coding: utf-8 -*-
"""
main.py
============================
The core file of my example project
"""

import argparse

import pandas as pd
import write_svg

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--mfi", type=str, help="Insert MFI file value (.xls)")
parser.add_argument("-t", "--template", help="Insert template file", type=str)
parser.add_argument("-o", "--output", help="output_prefix", type=str)

args = parser.parse_args()

svg_liste = [i for i in open(args.template, "r")]

edges_ligne, circle_ligne, text_ligne = write_svg.get_edges_dictionnary(svg_liste)

print(circle_ligne)
