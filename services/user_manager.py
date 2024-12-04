
from flask import request, session

class login:
  db=None
  
  username=""

  password=""

  def __init__(self,db):
    self.db = db
  
  def validate(self):
    pass

  def get_user_data(self):
    payload = {"username": self.username, "is_login": True, "msg": False}
    if(self.username != "admin"):
      payload['msg'] = "Username / Password salah"
      payload['is_login'] = False
    return payload
  
  def auth(self):
    self.username = request.form['username']
    self.password = request.form['password']
    
    # validasi input
    self.validate()

    #dapatkan data user
    user_data = self.get_user_data()
    if(user_data['is_login']):
      #membuat session
      session['token'] = user_data
    
    return user_data
pass

class logout:
  def destroy_token():
    session.pop('token', None)
    return True