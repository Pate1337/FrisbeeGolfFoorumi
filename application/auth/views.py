from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.roles.models import Role
from application.categories.models import Category
from application.topics.models import Topic
from application.messages.models import Message
from application.auth.forms import LoginForm, RegisterForm, ChangePassword, UserInfoForm

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

    # Create a role aswell
    r = Role()
    r.account_id = u.id

    db.session().add(r)
    db.session().commit()

    # Login straight away
    login_user(u)
    return redirect(url_for("categories_index"))

@app.route("/profile/<account_id>", methods = ["GET"])
def profile_show(account_id):
    user = User.query.get(account_id)
    latest_messages = Message.find_ten_latest_messages_by_user_id(user.id)
    latest_topics = Topic.find_ten_latest_topics_by_user_id(user.id)
    return render_template("auth/show.html", user = user, latest_messages = latest_messages, latest_topics = latest_topics)

@app.route("/profile/<account_id>/settings", methods = ["GET"])
@login_required(role="ANY")
def profile_settings(account_id):
    # Jos käyttäjä syöttää urliin toisen profiilin id:n, redirect oikeeseen (ei väliä oikeesti)
    if str(current_user.id) != str(account_id):
        return redirect(url_for('profile_settings', account_id = current_user.id))
    return render_template("auth/settings.html", user = current_user, form = UserInfoForm(), password_form = ChangePassword())

@app.route("/profile/<account_id>/delete", methods = ["POST"])
@login_required(role="ANY")
def profile_delete(account_id):
    # Tarkista että käyttäjän oma profiili
    if "ADMIN" not in current_user.get_roles():
        if str(current_user.id) != str(account_id):
            return redirect(url_for('profile_settings', account_id = current_user.id))
    
    # Hae user. Päivitä ennen jokaista jos tarve
    u = User.query.get(account_id)

    # Poista Category jonka account_id on account_id
    categories = u.categories
    for c in categories:
        c_topics = c.topics
        # Poista kategorian topicit
        for t in c_topics:
            c_t_messages = t.messages
            # Poista topicin viestit
            for m in c_t_messages:
                db.session().delete(m)
            db.session().delete(t)
        db.session().delete(c)

    # Poista Role jonka account_id on account_id
    roles = u.roles
    for r in roles:
        db.session().delete(r)

    # Poista Topic jonka account_id on account_id
    topics = u.topics
    for t in topics:
        t_messages = t.messages
        # Poista topicin viestit
        for m in t_messages:
            db.session().delete(m)
        db.session().delete(t)

    # Poista Message, jonka account_id on account_id
    messages = u.messages
    for m in messages:
        db.session().delete(m)
    
    # POISTA LOPUKSI USER
    db.session().delete(u)
    db.session().commit()

    return redirect(url_for('categories_index'))

@app.route("/profile/<account_id>/edit", methods = ["POST"])
@login_required(role="ANY")
def profile_edit_main(account_id):

    # Tarkista että käyttäjän oma profiili
    if str(current_user.id) != str(account_id):
        return redirect(url_for('profile_settings', account_id = current_user.id))
    
    form = UserInfoForm(request.form)

    if not form.validate():
      return render_template("auth/settings.html", user = current_user, form = form, password_form = ChangePassword(), error = 'Tietojen muuttaminen epäonnistui!')
    
    u = User.query.get(account_id)
    u.name = form.name.data
    u.username = form.username.data

    db.session().commit()

    return redirect(url_for('profile_show', account_id=account_id))

@app.route("/profile/<account_id>/change_password", methods = ["POST"])
@login_required(role="ANY")
def profile_change_password(account_id):

    # Tarkista että käyttäjän oma profiili
    if str(current_user.id) != str(account_id):
        return redirect(url_for('profile_settings', account_id = current_user.id))
    
    password_form = ChangePassword(request.form)

    if not password_form.validate():
      return render_template("auth/settings.html", user = current_user, form = UserInfoForm(), password_form = password_form, error = 'Salasanan vaihto epäonnistui!')
    
    u = User.query.get(account_id)

    if str(u.password) != str(password_form.old_password.data):
        return render_template("auth/settings.html", user = current_user, form = UserInfoForm(), password_form = password_form, password_error = 'Väärä salasana!', error = 'Salasanan vaihto epäonnistui!')
    
    u.password = password_form.new_password.data

    db.session().commit()

    return redirect(url_for('profile_show', account_id=account_id))

#@app.route("/search/<text>", methods=["GET"])
#def search_from_everywhere(text):
  # Search from messages
  #query = text.lower()
  #messages = Message.find_by_text(query)

  # Search from Topics by name and description
  # Search from Users by name or username
  # Search from Categories by name or description
