from flask import render_template

class guest_controller:
  db=None
  def __init__(self, db):
    self.db=db
  
  def dashboard(self):
    return render_template("guest.dashboard.html")