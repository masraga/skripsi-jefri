from flask import request, render_template, session, redirect
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
      if('msg' in session):
        self.error = session['msg']
        session.pop('msg', None)
      return render_template("sign-in.html", error=self.error)
    else:
      auth = self.login_service.auth()
      if(auth['is_login']):
        return render_template('index.html')
      else:
        session['msg'] = auth['msg']
        return redirect("/")
  
  def logout(self):
    logout_service.destroy_token()
    return render_template('sign-in.html')