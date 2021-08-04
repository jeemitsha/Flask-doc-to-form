from flask import Flask, render_template, redirect, request
import docx2txt
import zipfile
from lxml import etree
import pandas as pd
import os
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH = os.path.join(basedir, 'uploads'),
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*60*1000
)


def read_docx(docx_file, **kwargs):
    """Read tables as DataFrames from a Word document"""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(docx_file).open("word/document.xml") as f:
        root = etree.parse(f)
    for el in root.xpath("//w:tbl", namespaces=ns):
        el.tag = "table"
    for el in root.xpath("//w:tr", namespaces=ns):
        el.tag = "tr"
    for el in root.xpath("//w:tc", namespaces=ns):
        el.tag = "td"
    return pd.read_html(etree.tostring(root), **kwargs)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ["doc", "docx"]

dropzone = Dropzone(app)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")


@app.route("/form")
def form():
    data = read_docx("static\\test.docx")
    df = pd.DataFrame(data[0])
    df = df.dropna()
    df = df.reset_index(drop=True)
    text, images_path = docx2txt.process("static\\test.docx", "./static/img")
    q_list = []
    for i in range(0,len(df[1]),5):
        try:
            q_list.append([df[1][i],df[1][i+1],df[1][i+2],df[1][i+3],df[1][i+4]])
        except:
            break

    return render_template("form.html", imgpaths=images_path, questions=q_list)

if __name__ == "__main__":
    app.run(debug=True)
