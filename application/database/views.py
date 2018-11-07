from application import app, db
from flask import redirect, render_template, request, url_for
from application.database.models import Category

@app.route("/categories", methods=["GET"])
def categories_index():
    return render_template("categories/list.html", categories = Category.query.all())

@app.route("/categories/new/")
def categories_form():
    return render_template("categories/new.html")

@app.route("/categories/<category_id>/", methods=["POST"])
def categories_remove_description(category_id):

    c = Category.query.get(category_id)
    c.description = ""
    db.session().commit()
  
    return redirect(url_for("categories_index"))

@app.route("/categories/", methods=["POST"])
def categories_create():
    c = Category(request.form.get("name"), request.form.get("description"))

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("categories_index"))