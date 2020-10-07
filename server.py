from flask import Flask, render_template, request, redirect, url_for, abort
import os
import src.input_file_func as input_file_func
import src.hla_main as hla_main

app = Flask(__name__, static_folder="result")
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = [".xls",".xlsx"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)

        upload_filename = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(upload_filename)

        allele_type = input_file_func.check_parsing(upload_filename)
        args = hla_main.parse_args()
        args.gene=allele_type
        args.mfi=upload_filename
        output_list = input_file_func.find_output(filename, allele_type)

        hla_main.main(args)


    return render_template("index.html", data=output_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)