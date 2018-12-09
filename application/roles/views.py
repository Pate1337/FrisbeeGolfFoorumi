from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.roles.models import Role

@app.route("/roles/<account_id>/make/admin", methods=["POST"])
@login_required(role="ADMIN")
def toggle_role(account_id):
  r = Role.query.filter_by(account_id=account_id).first()
  print("ROLE: " + str(r.name))
  if r.name == "ADMIN":
    r.name = "USER"
  else:
    r.name = "ADMIN"
  
  db.session.commit()
  
  return redirect(url_for('application_statistics'))
