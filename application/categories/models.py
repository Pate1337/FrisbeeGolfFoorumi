from application import db
from application.models import Base
from sqlalchemy.sql import text

class Category(Base):

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    topics = db.relationship("Topic", backref='category_topic', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    @staticmethod
    def find_by_given_text(search_query):
        like_string = "%" + search_query + "%"
        stmt = text("SELECT id, name, description FROM category"
                    " WHERE (name LIKE :like_string OR description LIKE :like_string)")

        res = db.engine.execute(stmt, like_string=like_string)

        response = []
        for row in res:
            response.append({ "id": row[0], "name": row[1], "description": row[2] })
        return response