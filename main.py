import os, secrets
from flask import Flask
from dotenv import load_dotenv

from configs.database import database, migration, init_data

from controllers.user_controller import user_controller

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
  # new_migration.up() if os.getenv('DB_MIGRATE_TYPE') == "up" else new_migration.down()
  if os.getenv('DB_MIGRATE_TYPE') == "up":
    new_migration.up()
    new_init_data.run()
  else:
    new_migration.down()

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