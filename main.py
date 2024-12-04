import os, secrets
from flask import Flask, request, render_template, session

from configs.database import database

from controllers.user_controller import user_controller

# define database
db = database("localhost", "root", "")
db.connect()

#define controller
new_user_controller = user_controller(db)

#secret key
app_secret = secrets.token_urlsafe(16)

# define route
app = Flask(__name__, template_folder=os.path.abspath("views"), static_folder=os.path.abspath("public"))
app.secret_key = app_secret

@app.route("/", methods=['GET', 'POST'])
def login():
  return new_user_controller.login()

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  return new_user_controller.logout()