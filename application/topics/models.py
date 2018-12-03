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
                     " ON t.topic_id = m.topic_id ORDER BY latest DESC").params(category_id = category_id)
        # This would be good for finding the latest by date_modified
        #stmt = text("SELECT topic.name, topic.id AS topic_id, account.username, account.id AS account_id, messages.date_created AS latest FROM topic, account"
        #             " LEFT JOIN (SELECT * FROM message ORDER BY date_created ASC) messages"
        #             " ON messages.topic_id = topic.id"
        #             " WHERE category_id = :category_id AND topic.account_id = account.id"
        #             " GROUP BY topic.id ORDER BY latest DESC").params(category_id = category_id)

        # This relies heavily on GROUP BY returning the last record...Dunno why, but it does
        #stmt = text("SELECT topic.name, topic.id AS topic_id, account.username, account.id AS account_id, message.date_created AS latest FROM topic, account"
        #            " LEFT JOIN message ON message.topic_id = topic.id"
        #            " WHERE category_id = :category_id AND topic.account_id = account.id"
        #            " GROUP BY topic.id ORDER BY latest DESC").params(category_id = category_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            latest_message = ''
            if row[4]:
                latest_message = row[4]
            response.append({"topic":{ "name": row[0], "id": row[1], "latest_message": latest_message }, "account": { "username": row[2], "id": row[3] }})

        return response

# SELECT topic.name, topic.id AS topic_id, account.username, account.id AS account_id, messages.date_created AS latest FROM topic, account LEFT JOIN (SELECT * FROM message ORDER BY date_created ASC) messages ON messages.topic_id = topic.id WHERE category_id = 2 AND topic.account_id = account.id GROUP BY topic.id ORDER BY latest DESC

# SELECT t.id, m.maxDate FROM topic t LEFT JOIN (SELECT topic_id, max(date_created) AS maxDate FROM message GROUP BY topic_id) m ON t.id = m.topic_id WHERE t.category_id = 1

# SELECT t.topic_name, t.topic_id AS topic_id, t.username, t.topic_by_account AS account_id, m.maxDate AS latest FROM (SELECT topic.name AS topic_name, topic.id AS topic_id, account.id AS topic_by_account, account.username AS username FROM topic, account WHERE topic.account_id = account.id AND topic.category_id = 1) t LEFT JOIN (SELECT topic_id, max(date_created) AS maxDate FROM message GROUP BY topic_id) m ON t.topic_id = m.topic_id ORDER BY latest DESC