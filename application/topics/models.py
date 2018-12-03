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
        stmt = text("SELECT t.topic_name, t.topic_id AS topic_id, t.username, t.topic_by_account AS account_id, m.maxDate AS latest"
                     " FROM (SELECT topic.name AS topic_name, topic.id AS topic_id, account.id AS topic_by_account, account.username AS username FROM topic, account WHERE topic.account_id = account.id AND topic.category_id = :category_id) t"
                     " LEFT JOIN (SELECT topic_id, max(date_created) AS maxDate FROM message GROUP BY topic_id) m"
                     " ON t.topic_id = m.topic_id"
                     " ORDER BY CASE WHEN m.maxDate IS NULL THEN 1 ELSE 0 END, m.maxDate DESC").params(category_id = category_id)
        #stmt = text("SELECT q.topic_name, q.topic_id, q.topic_creator_username, q.topic_creator_id, q.latest, q.latest_message_user_id, a.username"
        #            " FROM (SELECT t.topic_name AS topic_name, t.topic_id AS topic_id, t.username AS topic_creator_username, t.topic_by_account AS topic_creator_id, m.maxDate AS latest, m.account_id AS latest_message_user_id FROM (SELECT topic.name AS topic_name, topic.id AS topic_id, account.id AS topic_by_account, account.username AS username FROM topic, account WHERE topic.account_id = account.id AND topic.category_id = :category_id) t"
        #            " LEFT JOIN (SELECT account_id, topic_id, max(date_created) AS maxDate FROM message GROUP BY account_id, topic_id) m"
        #            " ON t.topic_id = m.topic_id) q"
        #            " LEFT JOIN account a ON a.id = q.latest_message_user_id"
        #            " ORDER BY CASE WHEN q.latest IS NULL THEN 1 ELSE 0 END, q.latest DESC").params(category_id = category_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            latest_message = ''
            if row[4]:
                latest_message = row[4]
            response.append({"topic":{ "name": row[0], "id": row[1], "latest_message": latest_message }, "account": { "username": row[2], "id": row[3] }})

        return response

# SELECT q.topic_name, q.topic_id, q.topic_creator_username, q.topic_creator_id, q.latest, q.latest_message_user_id, a.username
#  FROM (SELECT t.topic_name AS topic_name, t.topic_id AS topic_id, t.username AS topic_creator_username, t.topic_by_account AS topic_creator_id, m.maxDate AS latest, m.account_id AS latest_message_user_id
#  FROM (SELECT topic.name AS topic_name, topic.id AS topic_id, account.id AS topic_by_account, account.username AS username
#  FROM topic, account WHERE topic.account_id = account.id AND topic.category_id = 2) t
#  LEFT JOIN (SELECT account_id, topic_id, max(date_created) AS maxDate FROM message GROUP BY topic_id) m
#  ON t.topic_id = m.topic_id AND m.account_id = t.latest_message_user_id) q
#  LEFT JOIN account a ON a.id = q.latest_message_user_id
#  ORDER BY CASE WHEN q.latest IS NULL THEN 1 ELSE 0 END, q.latest DESC

# SELECT q.topic_name, q.topic_id, q.topic_creator_username, q.topic_creator_id, q.latest, q.latest_message_user_id, a.username FROM (SELECT t.topic_name AS topic_name, t.topic_id AS topic_id, t.username AS topic_creator_username, t.topic_by_account AS topic_creator_id, m.maxDate AS latest, m.account_id AS latest_message_user_id FROM (SELECT topic.name AS topic_name, topic.id AS topic_id, account.id AS topic_by_account, account.username AS username FROM topic, account WHERE topic.account_id = account.id AND topic.category_id = 1) t LEFT JOIN (SELECT account_id, topic_id, max(date_created) AS maxDate FROM message GROUP BY account_id, topic_id) m ON t.topic_id = m.topic_id) q LEFT JOIN account a ON a.id = q.latest_message_user_id ORDER BY CASE WHEN q.latest IS NULL THEN 1 ELSE 0 END, q.latest DESC