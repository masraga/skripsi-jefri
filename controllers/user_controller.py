from flask import request, render_template, session, redirect, flash
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
        return render_template('index.html')
      else:
        flash(auth['msg'], 'danger')
        return redirect("/")
  
  def logout(self):
    logout_service.destroy_token()
    return render_template('sign-in.html')
  
  def guest_login(self):
    return render_template('sign_in_guest.html')