from flask import session, redirect

def is_auth_admin():
  is_admin = False
  if 'token' in session:
    if session['token']['username'] == 'admin':
      is_admin = True
  return is_admin

def redirect_admin_login():
  return redirect("/")