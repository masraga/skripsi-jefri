import os
from configs.database import database
from flask import Flask
from flask import render_template

# define database
db = database("localhost", "root", "")
db.connect()

# define route
app = Flask(__name__, template_folder=os.path.abspath("views"), static_folder=os.path.abspath("public"))

@app.route("/")
def hello_world():
  return render_template("index.html")