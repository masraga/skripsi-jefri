import mysql.connector

class database:
  host=""

  user=""

  password=""

  instance=None

  def __init__(self, host, user, password):
    self.host = host
    self.user = user
    self.password = password
  
  def connect(self):
    print("try to connect to mysql"); 
    try:  
      self.instance = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
      )
      print("mysql connect successfully")
    except mysql.connector.Error as err:
      raise Exception(err)