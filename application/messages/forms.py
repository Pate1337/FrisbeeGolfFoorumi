from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class MessageForm(FlaskForm):
    message = TextAreaField("Message", [validators.Length(min=1, message="Kentässä on oltava vähintään 1 merkki"), validators.Length(max=5000, message="Kentässä saa olla enintään 5000 merkkiä")])
 
    class Meta:
        csrf = False