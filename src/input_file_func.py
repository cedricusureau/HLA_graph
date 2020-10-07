import pandas as pd

def check_parsing(upload_file):
    df = pd.read_excel(upload_file)
    if len(df.columns) < 2:
        return "Parsing Error. Check input file syntax"
    if df.iloc[0][0][0][0] == "A":
        return "A B C"
    else :
        return "DR DQ DP"

def find_output_ABC(upload_file):
    file_name = upload_file.split(".")[0]
    return ["graph/{}.svg".format(file_name+"_A"),"graph/{}.svg".format(file_name+"_B"),"graph/{}.svg".format(file_name+"_C")]

def find_output_RQP(upload_file):
    file_name = upload_file.split(".")[0]
    return ["graph/{}.svg".format(file_name+"_DR"),"graph/{}.svg".format(file_name+"_DQ"),"graph/{}.svg".format(file_name+"_DP")]

def find_output(upload_file, allele_type):
    if allele_type == "A B C":
        return find_output_ABC(upload_file)
    else :
        return find_output_RQP(upload_file)
