from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CategoryForm(FlaskForm):
    name = StringField("Category name", [validators.Length(min=2)])

    # No need to validate description
    description = StringField("Category description")
 
    class Meta:
        csrf = False
