from flask import render_template, redirect
from services.user_manager import logout
from services.guest_info import guest_info

class guest_controller:
  db=None

  guest_info_service=None

  def __init__(self, db):
    self.db=db
    self.guest_info_service = guest_info(db)
  
  def dashboard(self):
    return render_template("guest.dashboard.html")
  
  def logout(self):
    l=logout(self.db)
    l.destroy_guest_token()
    return redirect("/")
  
  def guest_detail(self, id):
    guest=self.guest_info_service.get_list_guest(params={"id": id})
    if len(guest) == 0:
      return "User tidak ditemukan"
    guest=guest[0]
    face=self.guest_info_service.get_list_face(params={"guest_id": guest['id']})
    face=face[0]
    logs=self.guest_info_service.get_log(params={"guest_id": guest['id']})

    return render_template("guest.detail.html", guest=guest, face=face, logs=logs)