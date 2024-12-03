import os
from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder=os.path.abspath("views"), static_folder=os.path.abspath("public"))

@app.route("/")
def hello_world():
  return render_template("index.html")