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

@app.route('/A/')
def HLA_A():
    return render_template("HLA_A.html", data=[])

hla_A = """A*01:01,A*02:01,A*02:03,A*02:06,A*03:01,A*11:01,A*11:02,A*23:01,A*24:02,A*24:03,A*25:01,A*26:01,A*29:01,A*29:02,A*30:01,A*30:02,A*31:01,A*32:01,A*33:01,A*34:01,A*34:02,A*36:01,A*43:01,A*66:01,A*66:02,A*68:01,A*68:02,A*69:01,A*74:01,A*80:01,A*33:03"""

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #, ssl_context='adhoc')
