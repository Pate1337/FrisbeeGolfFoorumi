from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.categories.models import Category
from application.categories.forms import CategoryForm

@app.route("/categories", methods=["GET"])
def categories_index():
    #if current_user.is_authenticated:
    #  print("current_user.roles: " + str(current_user.roles))
    #  for r in current_user.roles:
    #    print("ROLE: " + r.name)
    #  print("current_user.getRoles(): " + str(current_user.get_roles()))
    return render_template("categories/list.html", categories = Category.query.all())

@app.route("/categories/new/")
@login_required(role="ADMIN")
def categories_form():
    return render_template("categories/new.html", form = CategoryForm())

#@app.route("/categories/<category_id>/", endpoint="remove_desc", methods=["POST"])
#@login_required
#def categories_remove_description(category_id):

#    c = Category.query.get(category_id)
#    c.description = ""
#    db.session().commit()
  
#    return redirect(url_for("categories_index"))

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