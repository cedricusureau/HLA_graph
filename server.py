from flask import Flask, render_template, request, abort
import os
import src.input_file_func as input_file_func
from src import hla_main as hla_main
import random
import pandas as pd

app = Flask(__name__, static_folder="result")
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = [".xls", ".xlsx"]


def process_file(upload_filename, filename, tresh):
    allele_type = input_file_func.check_parsing(upload_filename)
    args = hla_main.parse_args()
    args.gene = allele_type
    args.mfi = filename
    args.cutoff = int(tresh)
    output_list = input_file_func.find_output(filename, allele_type)

    hla_main.main_server(args)
    return output_list, allele_type


@app.route('/')
def index():
    return render_template("index.html", data=[])


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    tresh = request.form['tresh']
    filename = uploaded_file.filename

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = uploaded_file.filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
               uploaded_file.filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = uploaded_file.filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       uploaded_file.filename.split('.')[1]


        upload_filename = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(upload_filename)
        output_list, allele_type = process_file(upload_filename, filename, tresh)
        filename_wo_ext = filename.split(".")[0]
        file_csv = filename_wo_ext +".csv"
        file_html = filename_wo_ext +".html"
        return render_template("index.html", data=output_list, allele_type=allele_type.split(" "), file=file_csv, file_html=file_html)

    else:
        return render_template("index.html", data=[])


hla_A = """A*01:01,A*02:01,A*02:03,A*02:06,A*03:01,A*11:01,A*11:02,A*23:01,A*24:02,A*24:03,A*25:01,A*26:01,A*29:01,A*29:02,A*30:01,A*30:02,A*31:01,A*32:01,A*33:01,A*34:01,A*34:02,A*36:01,A*43:01,A*66:01,A*66:02,A*68:01,A*68:02,A*69:01,A*74:01,A*80:01,A*33:03"""
hla_B = """B*27:05,B*07:02,B*08:01,B*13:02,B*14:01,B*14:02,B*15:01,B*15:02,B*15:03,B*15:10,B*15:12,B*15:13,B*15:16,B*18:01,B*27:08,B*35:01,B*37:01,B*38:01,B*39:01,B*40:01,B*40:02,B*41:01,B*42:01,B*44:02,B*44:03,B*45:01,B*46:01,B*47:01,B*48:01,B*49:01,B*50:01,B*51:01,B*51:02,B*52:01,B*53:01,B*54:01,B*55:01,B*56:01,B*57:01,B*57:03,B*58:01,B*59:01,B*67:01,B*73:01,B*78:01,B*81:01,B*82:01,B*13:01,B*15:11,B*40:06"""
hla_C = """C*01:02,C*02:02,C*03:02,C*03:03,C*03:04,C*04:01,C*05:01,C*06:02,C*07:02,C*08:01,C*12:03,C*14:02,C*15:02,C*16:01,C*17:01,C*18:02"""
hla_DR = """DRB1*01:01,DRB1*01:02,DRB1*01:03,DRB1*03:01,DRB1*03:02,DRB1*04:01,DRB1*04:02,DRB1*04:04,DRB1*04:05,DRB1*07:01,DRB1*04:03,DRB1*08:01,DRB1*09:01,DRB1*09:02,DRB1*10:01,DRB1*11:01,DRB1*11:04,DRB1*12:01,DRB1*12:02,DRB1*13:01,DRB1*13:03,DRB1*14:01,DRB1*14:02,DRB1*14:54,DRB1*15:01,DRB1*15:02,DRB1*15:03,DRB1*16:01,DRB1*16:02"""
hla_DQ = """DQA1*02:01DQB1*02:01,DQA1*03:01DQB1*02:01,DQA1*04:01DQB1*02:01,DQA1*05:01DQB1*02:01,DQA1*02:01DQB1*02:02,DQA1*02:01DQB1*04:01,DQA1*03:03DQB1*04:01,DQA1*02:01DQB1*04:02,DQA1*04:01DQB1*04:02,DQA1*01:01DQB1*05:01,DQA1*01:02DQB1*05:02,DQA1*01:03DQB1*06:01,DQA1*01:02DQB1*06:02,DQA1*01:01DQB1*06:02,DQA1*01:03DQB1*06:03,DQA1*01:02DQB1*06:04,DQA1*01:02DQB1*06:09,DQA1*03:01DQB1*03:01,DQA1*02:01DQB1*03:01,DQA1*05:03DQB1*03:01,DQA1*05:05DQB1*03:01,DQA1*06:01DQB1*03:01,DQA1*02:01DQB1*03:02,DQA1*03:01DQB1*03:02,DQA1*03:02DQB1*03:02,DQA1*02:01DQB1*03:03,DQA1*03:01DQB1*03:03,DQA1*03:02DQB1*03:03"""
hla_DP = """DPA1*01:03DPB1*01:01,DPA1*02:01DPB1*01:01,DPA1*01:03DPB1*02:01,DPA1*02:02DPB1*05:01,DPA1*01:03DPB1*03:01,DPA1*01:05DPB1*03:01,DPA1*02:01DPB1*03:01,DPA1*01:03DPB1*04:01,DPA1*01:03DPB1*04:02,DPA1*02:01DPB1*05:01,DPA1*02:01DPB1*06:01,DPA1*01:03DPB1*06:01,DPA1*02:01DPB1*09:01,DPA1*02:02DPB1*10:01,DPA1*01:03DPB1*11:01,DPA1*01:03DPB1*28:01,DPA1*02:01DPB1*13:01,DPA1*02:02DPB1*13:01,DPA1*03:01DPB1*13:01,DPA1*02:01DPB1*14:01,DPA1*02:01DPB1*15:01,DPA1*02:01DPB1*17:01,DPA1*02:01DPB1*18:01,DPA1*01:05DPB1*18:01,DPA1*01:04DPB1*18:01,DPA1*01:03DPB1*19:01,DPA1*03:01DPB1*20:01,DPA1*01:03DPB1*23:01,DPA1*01:05DPB1*28:01,DPA1*04:01DPB1*28:01,DPA1*02:02DPB1*11:01"""

@app.route('/A/')
def HLA_A():
    return render_template("HLA_A.html", data=[])

@app.route('/A/', methods=['POST'])
def make_file_A():
    request_form = request.form
    data = {}
    for i in hla_A.split(","):
        data[i] = 0

    for i in request_form:
        data[i] = 7000

    filename="check_output.xls"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                   filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       filename.split('.')[1]

    df = pd.DataFrame({"allele":data.keys(), "mfi":data.values()})
    df.to_excel("uploads/{}".format(filename), index=False)

    output_list, allele_type = process_file("uploads/{}".format(filename), filename, 1000)
    filename_wo_ext = filename.split(".")[0]
    file_csv = filename_wo_ext + ".csv"
    file_html = filename_wo_ext + ".html"

    return render_template("HLA_A.html", data=output_list, allele_type="A", file=file_csv,
                           file_html=file_html)

@app.route('/B/')
def HLA_B():
    return render_template("HLA_B.html", data=[])

@app.route('/B/', methods=['POST'])
def make_file_B():
    print("coucou")
    request_form = request.form
    data = {}
    for i in hla_B.split(","):
        data[i] = 0

    for i in request_form:
        data[i] = 7000
    print(data)
    filename="check_output.xls"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                   filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       filename.split('.')[1]

    df = pd.DataFrame({"allele":data.keys(), "mfi":data.values()})
    df.to_excel("uploads/{}".format(filename), index=False)

    output_list, allele_type = process_file("uploads/{}".format(filename), filename, 1000)
    filename_wo_ext = filename.split(".")[0]
    file_csv = filename_wo_ext + ".csv"
    file_html = filename_wo_ext + ".html"

    return render_template("HLA_B.html", data=output_list, allele_type="A B C", file=file_csv,
                           file_html=file_html)

@app.route('/C/')
def HLA_C():
    return render_template("HLA_C.html", data=[])

@app.route('/C/', methods=['POST'])
def make_file_C():
    request_form = request.form
    data = {}
    for i in hla_C.split(","):
        data[i] = 0

    for i in request_form:
        data[i] = 7000

    filename="check_output.xls"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                   filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       filename.split('.')[1]

    df = pd.DataFrame({"allele":data.keys(), "mfi":data.values()})
    df.to_excel("uploads/{}".format(filename), index=False)

    output_list, allele_type = process_file("uploads/{}".format(filename), filename, 1000)
    filename_wo_ext = filename.split(".")[0]
    file_csv = filename_wo_ext + ".csv"
    file_html = filename_wo_ext + ".html"

    return render_template("HLA_C.html", data=output_list, allele_type="A B C", file=file_csv,
                           file_html=file_html)

@app.route('/DR/')
def HLA_DR():
    return render_template("HLA_DR.html", data=[])

@app.route('/DR/', methods=['POST'])
def make_file_DR():
    request_form = request.form
    data = {}
    for i in hla_DR.split(","):
        data[i] = 0

    for i in request_form:
        data[i] = 7000

    filename="check_output.xls"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                   filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       filename.split('.')[1]

    df = pd.DataFrame({"allele":data.keys(), "mfi":data.values()})
    df.to_excel("uploads/{}".format(filename), index=False)

    output_list, allele_type = process_file("uploads/{}".format(filename), filename, 1000)
    filename_wo_ext = filename.split(".")[0]
    file_csv = filename_wo_ext + ".csv"
    file_html = filename_wo_ext + ".html"

    return render_template("HLA_DR.html", data=output_list, allele_type="DR", file=file_csv,
                           file_html=file_html)

@app.route('/DQ/')
def HLA_DQ():
    return render_template("HLA_DQ.html", data=[])

@app.route('/DQ/', methods=['POST'])
def make_file_DQ():
    request_form = request.form
    data = {}
    for i in hla_DQ.split(","):
        data[i] = 0

    for i in request_form:
        data[i] = 7000

    filename="check_output.xls"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                   filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       filename.split('.')[1]

    df = pd.DataFrame({"allele":data.keys(), "mfi":data.values()})
    df.to_excel("uploads/{}".format(filename), index=False)

    output_list, allele_type = process_file("uploads/{}".format(filename), filename, 1000)
    filename_wo_ext = filename.split(".")[0]
    file_csv = filename_wo_ext + ".csv"
    file_html = filename_wo_ext + ".html"

    return render_template("HLA_DQ.html", data=output_list, allele_type="DR DQ DP", file=file_csv,
                           file_html=file_html)

@app.route('/DP/')
def HLA_DP():
    return render_template("HLA_DP.html", data=[])

@app.route('/DP/', methods=['POST'])
def make_file_DP():
    request_form = request.form
    data = {}
    for i in hla_DP.split(","):
        data[i] = 0

    for i in request_form:
        data[i] = 7000

    filename="check_output.xls"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                   filename.split('.')[1]

        while os.path.isfile("uploads/" + filename):
            filename = filename.split('.')[0] + "_" + str(random.randint(0, 1000)) + "." + \
                       filename.split('.')[1]

    df = pd.DataFrame({"allele":data.keys(), "mfi":data.values()})
    df.to_excel("uploads/{}".format(filename), index=False)

    output_list, allele_type = process_file("uploads/{}".format(filename), filename, 1000)
    filename_wo_ext = filename.split(".")[0]
    file_csv = filename_wo_ext + ".csv"
    file_html = filename_wo_ext + ".html"

    return render_template("HLA_DP.html", data=output_list, allele_type="DR DQ DP", file=file_csv,
                           file_html=file_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #, ssl_context='adhoc')
