from flask import render_template, redirect, url_for
from application import app, login_required
# from flask_login import current_user

from application.auth.models import User
from application.roles.models import Role
from application.categories.models import Category
from application.topics.models import Topic
from application.messages.models import Message
  
@app.route("/")
def hello():
    return redirect(url_for("categories_index"))

@app.route("/application/statistics", methods=["GET"])
@login_required(role="ADMIN")
def application_statistics():
  users = User.query.all()
  return render_template('statistics.html', users = users)

