import os, mysql.connector, hashlib
from dotenv import load_dotenv

load_dotenv(override=True)

class database:
  host=""

  user=""

  password=""

  name=""

  instance=None

  def __init__(self, host, user, password, name):
    self.host = host
    self.user = user
    self.password = password
    self.name = name
  
  def connect(self):
    print("try to connect to mysql"); 
    try:  
      self.instance = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
      )
      return self.instance
      print("mysql connect successfully")
    except mysql.connector.Error as err:
      raise Exception(err)
  
  def get_instance(self):
    return self.instance
  pass

class migration:
  db = None

  connector = None

  is_connect_db = False

  def __init__(self, db):
    self.db = db
    self.connector = db.cursor()
    self.check_db()
    pass

  def check_db(self):
    return self.connector.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.getenv('DB_NAME')))

  def up(self):
    self.db.database = os.getenv('DB_NAME')
    query = {
      self.user_table()['up']
    }
    for q in query: 
      self.db.cursor().execute(q)
    pass

  def down(self):
    self.db.database = os.getenv('DB_NAME')
    query = {
      self.user_table()['down']
    }
    for q in query:
      self.db.cursor().execute(q)
    pass

  def user_table(self):
    up = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), is_active TINYINT(1))"
    down = "DROP TABLE IF EXISTS users"
    return {"up": up, "down": down}
  pass

class init_data:
  db = None
  def __init__(self, db):
    self.db = db
    self.db.database = os.getenv('DB_NAME')

  def run(self):
    self.create_user()
    pass

  def create_user(self):
    user_cursor = self.db.cursor(dictionary=True)
    user_cursor.execute("SELECT * FROM users WHERE username='{}'".format(os.getenv('DB_USER_NAME')))
    user_cursor = user_cursor.fetchone()
    self.db.commit()
    if user_cursor == None:
      user_cursor = self.db.cursor()
      query = "INSERT INTO users (username, password, is_active) VALUES (%s, %s, %s)"
      query_value = (os.getenv('DB_USER_NAME'), hashlib.sha1(os.getenv('DB_USER_PASSWORD').encode()).hexdigest(), 1)
      user_cursor.execute(query, query_value)
      self.db.commit()
    pass