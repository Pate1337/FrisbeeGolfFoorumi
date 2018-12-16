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
  users = User.find_users_with_roles()
  return render_template('statistics.html', users = users)

@app.route("/search/<text>", methods=["GET"])
def search_from_everywhere(text):

  query = text.lower()

  messages = Message.find_by_given_text(query)

  topics = Topic.find_by_given_text(query)

  users = User.find_by_given_text(query)

  categories = Category.find_by_given_text(query)

  return render_template('search_results.html', text = text, messages = messages, topics = topics, users = users, categories = categories)

