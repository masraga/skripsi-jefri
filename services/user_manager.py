
import hashlib
from flask import request, session

class login:
  db=None
  
  username=""

  password=""

  user=None

  def __init__(self,db):
    self.db = db
  
  def validate(self):
    payload = {"username": self.username, "is_login": True, "msg": False}
    if self.user == None:
      payload['is_login']=False
      payload['msg']="Username / Password salah"
    
    return payload
  
  def get_user_data(self):
    user_cursor = self.db.cursor(dictionary=True)
    user_cursor.execute("SELECT * FROM users WHERE username='{}' and password='{}'".format(self.username, self.password));
    user = user_cursor.fetchone()
    self.user=user
    return user
  
  def auth(self):
    self.username = request.form['username']
    self.password = hashlib.sha1(request.form['password'].encode()).hexdigest()
    
    self.get_user_data()

    # validasi input
    validate = self.validate()

    #dapatkan data user
    if validate['is_login']:
      session['token'] = self.user

    return validate
pass  

class logout:
  def destroy_token():
    session.pop('token', None)
    return True