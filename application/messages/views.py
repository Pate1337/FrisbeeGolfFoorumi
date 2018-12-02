from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.messages.models import Message
from application.topics.models import Topic
from application.messages.forms import MessageForm

@app.route("/topics/<topic_id>/messages", methods=["GET"])
def messages_index(topic_id):
    # These could be done in one query
    # Search the topic by id
    t = Topic.query.get(topic_id)
    topic_messages = Message.find_messages_for_topic_with_users(topic_id)
    # will be form { message: { message: '', id: '' }, account: { username: '', id: '' } }
    return render_template("messages/list.html", messages = topic_messages, topic = t)

@app.route("/topics/<topic_id>/messages/new/")
@login_required
def messages_form(topic_id):
    return render_template("messages/new.html", form = MessageForm(), topic_id=topic_id)

@app.route("/topics/<topic_id>/messages/", methods=["POST"])
@login_required
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
