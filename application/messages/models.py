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
    stmt = text("SELECT m.message, m.id, m.date_created, m.date_modified, a.username, a.id FROM message m, account a"
                     " WHERE (m.topic_id = :topic_id AND m.account_id = a.id)"
                     " ORDER BY m.date_created DESC").params(topic_id = topic_id)
    res = db.engine.execute(stmt)

    response = []
    for row in res:
        response.append({"message":{ "message": row[0], "id": row[1], "created": row[2], "edited": row[3] }, "account": { "username": row[4], "id": row[5] }})

    return response
