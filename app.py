from flask import Flask, render_template, redirect


app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['doc', 'docx']

@app.route("/", methods=['GET', 'POST'])
def index():
    
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)