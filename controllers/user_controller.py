import os
from flask import request, render_template, session, redirect, flash, jsonify
from helpers.lbp import face_predict
from services.guest_info import guest_info
from services.user_manager import (
  login as login_service,
  logout as logout_service
)

class user_controller:
  db=None

  error=None

  def __init__(self, db):
    self.db = db
    self.login_service = login_service(db)
    # always remove msg session

  def login(self):
    req = request.form.to_dict()
    if 'process' not in req:
      return render_template("sign-in.html")
    else:
      auth = self.login_service.auth()
      if(auth['is_login']):
        guest_service=guest_info(self.db)
        overview=guest_service.get_yearly_user_total()
        return render_template('index.html', label=overview['label'], value=overview['value'])
      else:
        flash(auth['msg'], 'danger')
        return redirect("/")
  
  def logout(self):
    logout_service.destroy_token()
    return render_template('sign-in.html')
  
  def guest_login(self):
    if len(request.files.getlist('face')) == 0:
      return render_template('sign_in_guest.html')
    else: 
      upload_path="public/attempt"
      face_path="public/upload"
      face=request.files.getlist("face")[0]
      filename=os.path.join(upload_path, face.filename)
      face.save(filename)
      predict=face_predict(filename)
      os.remove(filename)
      if predict["is_error"] is not True:
        guest_service=guest_info(self.db)
        guest=guest_service.get_list_guest({"face_id": predict['face_id']})
        guest=guest[0]
        face_list=guest_service.get_list_face(params={"guest_id": guest["id"]})
        face=face_list[0]
        session["guest_token"]={
          "name": guest['name'],
          "face": os.path.join(face_path, face["face"]),
          "accuracy": predict["accuracy"]
        }
      return jsonify(predict)