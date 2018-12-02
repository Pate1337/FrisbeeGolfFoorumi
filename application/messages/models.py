from application import db
from application.models import Base
from sqlalchemy.sql import text

class Message(Base):

  message = db.Column(db.String(5000), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

  def __init__(self, message):
        self.message = message
  
  @staticmethod
  def find_messages_for_topic_with_users(topic_id):
    stmt = text("SELECT message.message, message.id AS message_id, account.username, account.id AS account_id FROM message, account"
                     " WHERE (topic_id = :topic_id AND message.account_id = account.id)").params(topic_id = topic_id)
    res = db.engine.execute(stmt)

    response = []
    for row in res:
        response.append({"message":{ "message": row[0], "id": row[1] }, "account": { "username": row[2], "id": row[3] }})

    return response
