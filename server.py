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

def extract_allele_liste(locus):
    file = open("data/nodes/HLA_{}_nodes.csv".format(locus))
    all_tmp = []
    for i in file:
        tmp = i.replace(", ","").replace("\n","")
        all_tmp.append(tmp)

    return ",".join(all_tmp)

hla_A = extract_allele_liste("A")
hla_B = extract_allele_liste("B")
hla_C = extract_allele_liste("C")
hla_DR = extract_allele_liste("DR")
hla_DQ = extract_allele_liste("DQ")
hla_DP = extract_allele_liste("DP")

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

    request_form = request.form
    data = {}
    for i in hla_B.split(","):
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
    test = request_form["test"]
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
