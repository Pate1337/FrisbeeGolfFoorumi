from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.topics.models import Topic
from application.categories.models import Category
from application.topics.forms import TopicForm

@app.route("/categories/<category_id>/topics", methods=["GET"])
def topics_index(category_id):
    # Search the category by id
    c = Category.query.get(category_id)

    category_topics = Topic.find_topics_for_category_with_users(category_id, "created", "desc")
    # will be form {"topic":{ "id": row[0], "name": row[1], "created": row[2], "creator_username": row[3], "creator_id": row[4] }, "latest_message": { "created": latest_message_created, "creator_username": latest_message_creator_username, "creator_id": latest_message_creator_id }}
    
    return render_template("topics/list.html", topics = category_topics, category = c, order_by = "created", order = "desc")

@app.route("/categories/<category_id>/topics/new/", endpoint="topic_creation", methods=["GET"])
@login_required(role="ANY")
def topics_form(category_id):
    return render_template("topics/new.html", form = TopicForm(), category_id=category_id)

@app.route("/categories/<category_id>/topics/create", endpoint="add_new_topic", methods=["POST"])
@login_required(role="ANY")
def topics_create(category_id):
    form = TopicForm(request.form)

    if not form.validate():
      return render_template("topics/new.html", form = form, category_id=category_id)
    
    t = Topic(form.name.data, form.description.data)
    t.account_id = current_user.id
    t.category_id = category_id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("topics_index", category_id=category_id))

@app.route("/categories/<category_id>/topics/", methods=["POST"])
def topics_sort(category_id):
  c = Category.query.get(category_id)

  # Huikeeta hakkerointia :D
  order_by = request.form['order_by']
  order = request.form['order']

  category_topics = Topic.find_topics_for_category_with_users(category_id, order_by, order)
  return render_template("topics/list.html", topics = category_topics, category = c, order_by = order_by, order = order)
