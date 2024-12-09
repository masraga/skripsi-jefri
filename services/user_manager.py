
import hashlib, random, string
from flask import request, session, url_for
from repositories.guest_repo import guest_repo

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
      session['token'] = validate

    return validate
pass  

class logout:
  def destroy_token():
    session.pop('token', None)
    return True
  
class user:
  db=None

  username=""

  images=[]

  gender=""

  allowed_file=["jpg", "jpeg", "png"]

  guest_repo=None

  def __init__(self, db, username, images, gender):
    self.db = db
    self.username = username
    self.images = images
    self.gender=gender
    self.guest_repo=guest_repo(db)
    return
  
  def validation(self):
    # validasi gambar
    return {"is_error": False,  "msg": ""}
  
  def set_payload(self):
    face_id=''.join(random.choices(string.ascii_letters,k=7))
    payload = {"username": self.username, "faces": [], "face_id": face_id, "gender": self.gender}
    for index in range(len(self.images)):
      ext = self.images[index].filename.rsplit(".", 1)[1]
      filename = f'{face_id}-{index}.{ext}'
      payload["faces"].append(filename)
      self.images[index].save(f'public/upload/{filename}')
    
    return payload

  def create(self):
    self.validation()
    if(self.validation()['is_error']):
      return self.validation()
    
    payload = self.set_payload()
    self.guest_repo.create(payload["username"], payload["faces"], payload['face_id'], payload['gender'])    

    result = {"is_error": False, "msg": "Data user berhasil disimpan", "msg_type": "success"}
    return result