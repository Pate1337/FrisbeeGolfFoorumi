from flask import render_template, redirect, url_for
from application import app
  
@app.route("/")
def hello():
    return redirect(url_for("categories_index"))
