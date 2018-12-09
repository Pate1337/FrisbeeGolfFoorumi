from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class CategoryForm(FlaskForm):
    name = StringField("Category name", [validators.Length(min=2, message="Kentässä on oltava vähintään 2 merkkiä")])

    # No need to validate description
    description = TextAreaField("Category description", [validators.Length(max=1000, message="Kentässä saa olla enintään 1000 merkkiä")])
 
    class Meta:
        csrf = False
