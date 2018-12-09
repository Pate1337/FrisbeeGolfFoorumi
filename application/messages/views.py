from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.messages.models import Message
from application.topics.models import Topic
from application.categories.models import Category
from application.messages.forms import MessageForm

@app.route("/topics/<topic_id>/messages", methods=["GET"])
def messages_index(topic_id):
    t = Topic.find_topic_with_creator_info(topic_id)
    # will be form [{ "name": '', "id": '', "date_created": row[2], "date_modified": row[3], "desription": row[4], "category_id": row[5], "account": {"id": row[6], "username": row[7]} }]
    c = Category.query.get(t[0]["category_id"])
    topic_messages = Message.find_messages_for_topic_with_users(topic_id)
    # will be form { message: { message: '', id: '' }, account: { username: '', id: '' } }
    return render_template("messages/list.html", messages = topic_messages, topic = t[0], category = c)

@app.route("/topics/<topic_id>/messages/new/", endpoint="message_creation", methods=["GET"])
@login_required(role="ANY")
def messages_form(topic_id):
    return render_template("messages/new.html", form = MessageForm(), topic_id=topic_id)

@app.route("/topics/<topic_id>/messages", endpoint="add_new_message", methods=["POST"])
@login_required(role="ANY")
def messages_create(topic_id):
    form = MessageForm(request.form)

    if not form.validate():
      return render_template("messages/new.html", form = form, topic_id=topic_id)
    
    m = Message(form.message.data)
    m.account_id = current_user.id
    m.topic_id = topic_id

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("messages_index", topic_id=topic_id))

@app.route("/messages/<message_id>/delete", methods=["POST"])
@login_required(role="ANY")
def messages_delete(message_id):
  m = Message.query.get(message_id)
  topic_id = m.topic_id

  if "ADMIN" not in current_user.get_roles():
    if str(m.account_id) != str(current_user.id):
      return redirect(url_for('messages_index', topic_id = topic_id))
  
  # if user is ADMIN or the creator of the message
  db.session().delete(m)
  db.session().commit()

  return redirect(url_for('messages_index', topic_id = topic_id))

@app.route("/messages/<message_id>/edit", methods=["GET", "POST"])
@login_required(role="ANY")
def messages_edit(message_id):
  m = Message.query.get(message_id)
  topic_id = m.topic_id

  if str(m.account_id) != str(current_user.id):
    return redirect(url_for('messages_index', topic_id = topic_id))
  
  if request.method == "GET":
    form = MessageForm()
    form.message.data = m.message
    return render_template("messages/edit.html", form = form, message = m)
  
  # If POST
  form = MessageForm(request.form)

  if not form.validate():
    return render_template("messages/edit.html", form = form, message = m)
    
  m.message = form.message.data

  db.session().commit()

  return redirect(url_for("messages_index", topic_id=topic_id))
