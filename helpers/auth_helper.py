from flask import session, redirect

def is_auth_admin():
  is_admin = False
  if 'token' in session:
    if session['token']['username'] == 'admin':
      is_admin = True
  return is_admin

def is_auth_guest():
  is_guest = False
  if 'guest_token' in session:
    if session["guest_token"]['guest_id'] is not None:
      is_guest = True
  return is_guest

def redirect_admin_login():
  return redirect("/admin")

def redirect_guest_login():
  return redirect("/")