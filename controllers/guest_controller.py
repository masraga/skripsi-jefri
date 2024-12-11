from flask import render_template, redirect
from services.user_manager import logout

class guest_controller:
  db=None
  def __init__(self, db):
    self.db=db
  
  def dashboard(self):
    return render_template("guest.dashboard.html")
  
  def logout(self):
    l=logout(self.db)
    l.destroy_guest_token()
    return redirect("/")