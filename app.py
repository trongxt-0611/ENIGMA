from flask import Flask, render_template, request,send_file
from flask_bootstrap import Bootstrap5
from  enigma import encode
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
bootstrap = Bootstrap5(app)


def upload_file(request):
  f = request.files['settings']
  f.save(secure_filename(f.filename))
  return open_file(secure_filename(f.filename))

def open_file(file_name):
  f = open(file_name, "r")
  lines = []
  for x in f:
   value = x.strip('\n').split('=')[1].replace('"','')
   lines.append(value)
  return lines


@app.route("/")
def hello_world():
    return render_template('index.html',req="", res="")

@app.route('/download')
def download():
    path = 'settings_sample.txt'
    return send_file(path, as_attachment=True)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    settings = ['I,II,III', 'UKW-B', 'ABC', 'DEF', 'AT BS DE FM IR KN LZ OW PV XY']
    if request.files['settings']:
     settings = upload_file(request)
    input_text = request.form['input_text']
    res = encode(input_text, settings)
    return render_template('index.html', req = input_text,res=res)

if __name__ == "__main__":
  app.run(debug=True)
