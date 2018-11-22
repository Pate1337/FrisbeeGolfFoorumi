from flask_wtf import FlaskForm
from wtforms import StringField, validators

class TopicForm(FlaskForm):
    name = StringField("Topic name", [validators.Length(min=2)])
 
    class Meta:
        csrf = False
