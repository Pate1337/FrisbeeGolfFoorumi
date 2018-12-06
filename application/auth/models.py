from application import db
from application.models import Base

class User(Base):

    __tablename__ = "account"
  
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    categories = db.relationship("Category", backref='account', lazy=True)
    topics = db.relationship("Topic", backref='topic', lazy=True)
    messages = db.relationship("Message", backref='user_message', lazy=True)
    roles = db.relationship("Role", backref="role", lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def get_roles(self):
        role_names = []
        for r in self.roles:
            role_names.append(r.name)
        return role_names
    