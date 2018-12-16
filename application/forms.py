from flask_wtf import FlaskForm
from wtforms import StringField, validators

class SearchForm(FlaskForm):
    query = StringField("Search", [validators.Length(min=1, message="Kentässä on oltava vähintään 1 merkki"), validators.Length(max=20)])
 
    class Meta:
        csrf = False