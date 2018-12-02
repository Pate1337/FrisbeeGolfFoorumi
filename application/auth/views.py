from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    login_form = LoginForm(request.form)
    # mahdolliset validoinnit
    if not login_form.validate():
      return render_template("auth/loginform.html", form = login_form)

    user = User.query.filter_by(username=login_form.username.data, password=login_form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = login_form,
                                error = "No such username or password")


    login_user(user)
    return redirect(url_for("categories_index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("categories_index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())
    
    register_form = RegisterForm(request.form)

    if not register_form.validate():
      return render_template("auth/registerform.html", form = register_form)
    
    user = User.query.filter_by(username=register_form.username.data).first()
    if user:
        return render_template("auth/registerform.html", form = register_form, error = "Username already taken!")
    
    # Everything ok, create new user
    u = User(register_form.name.data, register_form.username.data, register_form.password.data)

    db.session().add(u)
    db.session().commit()
    
    # Login straight away
    login_user(u)
    return redirect(url_for("categories_index"))

@app.route("/profile/<account_id>", methods = ["GET"])
def profile_show(account_id):
    if not current_user.is_authenticated:
        user = User.query.get(account_id)
        return render_template("auth/show.html", user = user, own_profile = False)

    if str(current_user.id) == str(account_id):
        return render_template("auth/show.html", user = current_user, own_profile = True)

    user = User.query.get(account_id)
    return render_template("auth/show.html", user = user, own_profile = False)
