from flask import request, flash, render_template, request

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