from flask import Flask, render_template, request, redirect, flash, jsonify

from parser.Parser import Parser
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
    parser = Parser()
    result = parser.parse_file("temp_file.CMP")

    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            p = Parser()
            res = p.parse_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # f = open(os.path.join(
            #     app.config['UPLOAD_FOLDER'], filename))
            # f.read()

            return render_template("index.html", header=res.get("header"), carrier=res.get("carrier"),  ULDs=res.get("ULDs"))
            # return jsonify(res)
            #return redirect(url_for('download_file', name=filename))

    # method == 'GET'
    else:
        return render_template('index.html')
        # return '''
        # <!doctype html>
        # <title>Upload new File</title>
        # <h1>Upload new File</h1>
        # <form method=post enctype=multipart/form-data>
        # <input type=file name=file>
        # <input type=submit value=Upload>
        # </form>
        # '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


