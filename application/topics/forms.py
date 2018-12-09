from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class TopicForm(FlaskForm):
    name = StringField("Topic name", [validators.Length(min=2, message="Kentässä on oltava vähintään 2 merkkiä"), validators.Length(max=144, message="Kentässä saa olla enintään 144 merkkiä")])
    description = TextAreaField("Topic description", [validators.Length(max=5000, message="Kentässä saa olla enintään 5000 merkkiä")])
 
    class Meta:
        csrf = False
