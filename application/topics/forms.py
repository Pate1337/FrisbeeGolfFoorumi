from flask_wtf import FlaskForm
from wtforms import StringField, validators

class TopicForm(FlaskForm):
    name = StringField("Topic name", [validators.Length(min=2), validators.Length(max=144)])
    description = StringField("Topic description", [validators.Length(max=5000)])
 
    class Meta:
        csrf = False
