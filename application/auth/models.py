from application import db
from application.models import Base
from sqlalchemy.sql import text

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
    
    @staticmethod
    def find_users_with_roles():
        stmt = text("SELECT a.id, a.date_created, a.date_modified, a.username, a.name, r.id, r.name"
                " FROM account a, role r"
                " WHERE a.id = r.account_id")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({ "id": row[0], "date_created": row[1], "date_modified": row[2], "username": row[3], "name": row[4], "role": { "id": row[5], "name": row[6] } })
        return response
    
    @staticmethod
    def find_by_given_text(search_query):
        like_string = "%" + search_query + "%"
        stmt = text("SELECT id, username FROM account"
                    " WHERE (username LIKE :like_string OR name LIKE :like_string)")

        res = db.engine.execute(stmt, like_string=like_string)

        response = []
        for row in res:
            response.append({ "id": row[0], "username": row[1] })
        return response
    