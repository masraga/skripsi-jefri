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
    self.check_db()
    pass

  def check_db(self):
    cursor = self.db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.getenv('DB_NAME')))
    self.db.commit()
    return True

  def up(self):
    self.db.database = os.getenv('DB_NAME')
    cursor = self.db.cursor(buffered=True)
    query = [
      self.user_table()['up'],
      self.guest_table()['up'],
      self.guest_face_table()['up'],
    ]
    for q in query:
      cursor.execute(q)
      self.db.commit()

  def down(self):
    self.db.database = os.getenv('DB_NAME')
    query = {
      self.user_table()['down'],
      self.guest_table()['down'],
      self.guest_face_table()['down']
    }
    for q in query:
      self.db.cursor().execute(q)
    self.db.commit()

  def user_table(self):
    up = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), is_active TINYINT(1))"
    down = "DROP TABLE IF EXISTS users"
    return {"up": up, "down": down}
  pass

  def guest_table(self):
    up = """
      CREATE TABLE IF NOT EXISTS guests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        face_id VARCHAR(255),
        is_active TINYINT DEFAULT 1
      )
    """

    down = """
      DROP TABLE IF EXISTS guests;
    """
    return {"up": up, "down": down}

  def guest_face_table(self):
    up = """
      CREATE TABLE IF NOT EXISTS guest_faces (
        id INT AUTO_INCREMENT PRIMARY KEY,
        guest_id INT,
        face VARCHAR(255),
        is_active TINYINT DEFAULT 1
      );
    """

    down = """
      DROP TABLE IF EXISTS guest_faces;
    """
    return {"up": up, "down": down}
  
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