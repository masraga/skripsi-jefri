from flask import request, flash, render_template, request, redirect, session
from services.user_manager import user as user_service

class admin_controller:
  
  db=None

  def __init__(self, db):
    self.db = db

  def dashboard(self):
    return render_template("index.html")

  def user(self, path=None):
    if path == None:
      return render_template("user.html")
    else:
      if path == "add":
        return render_template("new_user_form.html")
      elif path == 'save':
        faces = request.files.getlist('face[]')
        face_list = []
        for face in faces:
          face_list.append(face)
        req_user = user_service(self.db, request.form["username"], face_list).create()
        flash(req_user['msg'], req_user['msg_type'])
        return redirect("/admin/user/new_user")