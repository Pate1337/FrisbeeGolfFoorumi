from application import db
from application.models import Base
from sqlalchemy.sql import text

class Topic(Base):

    name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    messages = db.relationship("Message", backref='topic_message', lazy=True)
    description = db.Column(db.String(5000), nullable=False)

    def __init__(self, name, description = ""):
        self.name = name
        self.description = description
    
    @staticmethod
    def find_topics_for_category_with_users(category_id, order_by, order):
        #stmt = text("SELECT t.topic_name, t.topic_id AS topic_id, t.username, t.topic_by_account AS account_id, m.maxDate AS latest"
        #             " FROM (SELECT topic.name AS topic_name, topic.id AS topic_id, account.id AS topic_by_account, account.username AS username FROM topic, account WHERE topic.account_id = account.id AND topic.category_id = :category_id) t"
        #             " LEFT JOIN (SELECT topic_id, max(date_created) AS maxDate FROM message GROUP BY topic_id) m"
        #             " ON t.topic_id = m.topic_id"
        #             " ORDER BY CASE WHEN m.maxDate IS NULL THEN 1 ELSE 0 END, m.maxDate DESC").params(category_id = category_id)
        stmt = Topic.determine_query(category_id, order_by, order)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            latest_message_created = ''
            latest_message_creator_username = ''
            latest_message_creator_id = ''
            if row[5]:
                latest_message_created = row[5]
                latest_message_creator_username = row[6]
                latest_message_creator_id = row[7]
            response.append({"topic":{ "id": row[0], "name": row[1], "created": row[2], "creator_username": row[3], "creator_id": row[4] }, "latest_message": { "created": latest_message_created, "creator_username": latest_message_creator_username, "creator_id": latest_message_creator_id }})

        return response
    
    def determine_query(category_id, order_by, order):
        if order_by == 'latest_message':
            if order == 'desc':
                order_query = " ORDER BY CASE WHEN t.latest_message IS NULL THEN 1 ELSE 0 END, t.latest_message DESC"
            else:
                order_query = " ORDER BY CASE WHEN t.latest_message IS NULL THEN 1 ELSE 0 END, t.latest_message ASC"
        elif order_by == 'created':
            if order == 'desc':
                order_query = " ORDER BY e.topic_date_created DESC"
            else:
                order_query = " ORDER BY e.topic_date_created ASC"
        main_text = text("SELECT e.topic_id, e.topic_name, e.topic_date_created, e.topic_creator_username, e.topic_creator_id, t.latest_message, t.message_creator_username, t.message_creator_id"
                    " FROM ("
                    "SELECT t.id AS topic_id, t.name AS topic_name, t.date_created AS topic_date_created, a.username AS topic_creator_username, a.id AS topic_creator_id"
                    " FROM topic t, account a"
                    " WHERE t.category_id = :category_id AND a.id = t.account_id"
                    ") e LEFT JOIN ("
                    "SELECT m.topic_id AS topic_id, a.username AS message_creator_username, h.max AS latest_message, a.id AS message_creator_id"
                    " FROM ("
                    "SELECT topic_id, max(date_created) AS max FROM message GROUP BY topic_id"
                    ") h, message m, account a"
                    " WHERE m.topic_id = h.topic_id"
                    " AND m.account_id = a.id"
                    " AND h.max = m.date_created"
                    ") t ON e.topic_id = t.topic_id"
                    + order_query).params(category_id = category_id)
        return main_text

# FINAL QUERY :DD
# SELECT e.topic_id, e.topic_name, e.topic_date_created, e.topic_creator_username, e.topic_creator_id, t.latest_message, t.message_creator_username, t.message_creator_id
#  FROM (
# SELECT t.id AS topic_id, t.name AS topic_name, t.date_created AS topic_date_created, a.username AS topic_creator_username, a.id AS topic_creator_id
#  FROM topic t, account a
#  WHERE t.category_id = 2 AND a.id = t.account_id
# ) e LEFT JOIN (
# SELECT m.topic_id AS topic_id, a.username AS message_creator_username, h.max AS latest_message, a.id AS message_creator_id
#  FROM (
# SELECT topic_id, max(date_created) AS max FROM message GROUP BY topic_id
# ) h, message m, account a
#  WHERE m.topic_id = h.topic_id
#  AND m.account_id = a.id
#  AND h.max = m.date_created
# ) t ON e.topic_id = t.topic_id
#  ORDER BY CASE WHEN t.latest_message IS NULL THEN 1 ELSE 0 END, t.latest_message DESC;