from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.topics.models import Topic
from application.categories.models import Category
from application.topics.forms import TopicForm

@app.route("/categories/<category_id>/topics/", methods=["GET"])
def topics_index(category_id):
    # Tässä tarttee hakea vaan categoryn id:n perusteella Topics
    # Categorylle on määritelty relationship topicseihein Modeleissa
    category_topics = Category.query.get(category_id).topics
    return render_template("topics/list.html", topics = category_topics, category_id = category_id)

@app.route("/categories/<category_id>/topics/new/")
@login_required
def topics_form(category_id):
    return render_template("topics/new.html", form = TopicForm(), category_id=category_id)

@app.route("/categories/<category_id>/topics/", methods=["POST"])
@login_required
def topics_create(category_id):
    form = TopicForm(request.form)

    if not form.validate():
      return render_template("topics/new.html", form = form, category_id=category_id)
    
    t = Topic(form.name.data)
    t.account_id = current_user.id
    t.category_id = category_id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("topics_index", category_id=category_id))