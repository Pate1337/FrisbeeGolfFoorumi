from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.categories.models import Category
from application.categories.forms import CategoryForm

@app.route("/categories", methods=["GET"])
def categories_index():
    return render_template("categories/list.html", categories = Category.query.all())

@app.route("/categories/new/")
@login_required(role="ADMIN")
def categories_form():
    return render_template("categories/new.html", form = CategoryForm())

@app.route("/categories/", endpoint="categories_create", methods=["POST"])
@login_required(role="ADMIN")
def categories_create():
    form = CategoryForm(request.form)

    if not form.validate():
      return render_template("categories/new.html", form = form)
    
    c = Category(form.name.data, form.description.data)
    c.account_id = current_user.id

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("categories_index"))
  
@app.route("/categories/<category_id>/delete", methods=["POST"])
@login_required(role="ADMIN")
def categories_delete(category_id):
  print("Poistetaan kategoria id: " + category_id)
  c = Category.query.get(category_id)

  for t in c.topics:
    t_messages = t.messages
    for m in t_messages:
      db.session().delete(m)
    db.session().delete(t)
  
  db.session().delete(c)
  db.session().commit()

  return redirect(url_for('categories_index'))
