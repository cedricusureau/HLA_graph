from flask import Flask, render_template, request, abort
import os
import src.input_file_func as input_file_func
from src import hla_main as hla_main
import random

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #, ssl_context='adhoc')
