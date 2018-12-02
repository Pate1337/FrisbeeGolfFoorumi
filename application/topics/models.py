from application import db
from application.models import Base
from sqlalchemy.sql import text

class Topic(Base):

    name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    messages = db.relationship("Message", backref='topic_message', lazy=True)

    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def find_topics_for_category_with_users(category_id):
        stmt = text("SELECT topic.name, topic.id AS topic_id, account.username, account.id AS account_id FROM topic, account"
                     " WHERE (category_id = :category_id AND topic.account_id = account.id)").params(category_id = category_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"topic":{ "name": row[0], "id": row[1] }, "account": { "username": row[2], "id": row[3] }})

        return response