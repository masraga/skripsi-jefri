from flask import request, flash, render_template, request, redirect, session
from services.user_manager import user as user_service
from services.guest_info import guest_info
from helpers.auth_helper import is_auth_admin, redirect_admin_login

class admin_controller:
  
  db=None

  def __init__(self, db):
    self.db = db

  def dashboard(self):
    if not is_auth_admin(): return redirect_admin_login()
    return render_template("index.html")

  def user(self, path=None):
    # if not is_auth_admin(): return redirect_admin_login() 
    guest_service=guest_info(self.db)
    if path == None:
      guest_list=guest_service.get_list_guest()
      return render_template("user.html", guest_list=guest_list)
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
      elif path == 'detail':
        guest_id=request.args.get("id")
        faces=guest_service.get_list_face({"guest_id": guest_id})
        print(faces)
        return "Tampilkan detaul"