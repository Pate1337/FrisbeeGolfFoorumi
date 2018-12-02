from flask_wtf import FlaskForm
from wtforms import StringField, validators

class MessageForm(FlaskForm):
    message = StringField("Message", [validators.Length(min=1), validators.Length(max=5000)])
 
    class Meta:
        csrf = False