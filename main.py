import os, secrets
from flask import Flask
from dotenv import load_dotenv

from configs.database import database, migration, init_data
from configs.upload_file import upload_file

from controllers.user_controller import user_controller
from controllers.admin_controller import admin_controller
from controllers.guest_controller import guest_controller

#load env
load_dotenv()

# define database
db = database(
  os.getenv('DB_HOST'), 
  os.getenv('DB_USER'), 
  os.getenv('DB_PASSWORD'), 
  os.getenv('DB_NAME')
)

#run migration
if(os.getenv('DB_MIGRATE')):
  new_migration = migration(db.connect())
  new_init_data = init_data(db.connect())
  if os.getenv('DB_MIGRATE_TYPE') == "up":
    new_migration.up()
    new_init_data.run()
  else:
    new_migration.down()

#define lib
new_upload_file = upload_file()
new_upload_file.run()

#define controller
db = db.connect()
db.database = os.getenv("DB_NAME")
new_user_controller = user_controller(db)
new_admin_controller = admin_controller(db)
new_guest_controller = guest_controller(db)

#secret key
app_secret = secrets.token_urlsafe(16)

# define route
app = Flask(__name__, template_folder=os.path.abspath("views"), static_folder=os.path.abspath("public"))
app.secret_key = app_secret
app.config['UPLOAD_FOLDER'] = "public/upload"

@app.route("/admin", methods=['GET', 'POST'])
def login():
  return new_user_controller.login()

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  return new_user_controller.logout()

@app.route("/admin/dashboard", methods=['GET'])
def dashboard():
  return new_admin_controller.dashboard()

@app.route("/admin/user", methods=['GET'])
def user():
  return new_admin_controller.user()

@app.route("/admin/user/new_user", methods=['GET'])
def new_user():
  return new_admin_controller.user("add")

@app.route("/admin/user/save_user", methods=['POST'])
def save_user():
  return new_admin_controller.user("save")

@app.route("/admin/user/detail", methods=['GET'])
def user_detail():
  return new_admin_controller.user("detail")

@app.route("/", methods=['GET', 'POST'])
def guest_login():
  return new_user_controller.guest_login()

@app.route("/guest", methods=['GET', 'POST'])
def guest_dashboard():
  return new_guest_controller.dashboard()

@app.route("/guest/logout", methods=['GET', 'POST'])
def guest_logout():
  return new_guest_controller.logout()

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5000', debug=True)