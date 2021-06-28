import pandas as pd

def check_parsing(upload_file):

    df = pd.read_excel(upload_file)
    if len(df.columns) == 2:
        if ("A*" in str(df.columns[0])) or ("B*" in str(df.columns[0])) or ("C*" in str(df.columns[0])) or ("DR*" in str(df.columns[0])):
            first_row = list(df.columns)
            df = pd.read_excel(upload_file, names = ["Allele","Mfi"], header = None)
            df = df.append({"Allele":first_row[0],"Mfi":first_row[1]}, ignore_index = True)

    elif len(df.columns) == 3:
        if ("DR*" in str(df.columns[0])) or ("DQ*" in str(df.columns[0]))or ("DP*" in str(df.columns[0])):
            first_row = list(df.columns)
            df = pd.read_excel(upload_file, names = ["Allele","Allele2","Mfi"], header = None)
            df = df.append({"Allele":first_row[0],"Allele2":first_row[1], "Mfi":first_row[2]}, ignore_index = True)

    if len(df.columns) < 2:
        return "Parsing Error. Check input file syntax"

    if (str(df[df.columns[0]][0][0]) == "A") or (str(df[df.columns[0]][0][0]) == "B") or (str(df[df.columns[0]][0][0]) == "C"):
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
