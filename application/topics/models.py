from application import db
from application.models import Base
from sqlalchemy.sql import text

class Topic(Base):

    name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    messages = db.relationship("Message", backref='topic_message', lazy=True)
    description = db.Column(db.String(5000))

    def __init__(self, name, description = ""):
        self.name = name
        self.description = description
    
    @staticmethod
    def find_topics_for_category_with_users(category_id, order_by, order):
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
    
    @staticmethod
    def find_topic_with_creator_info(topic_id):
        stmt = text("SELECT t.name, t.id, t.date_created, t.date_modified, t.description, t.category_id, a.id, a.username"
                    " FROM topic t, account a WHERE t.id = :topic_id"
                    " AND t.account_id = a.id").params(topic_id = topic_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({ "name": row[0], "id": row[1], "date_created": row[2], "date_modified": row[3], "description": row[4], "category_id": row[5], "account": {"id": row[6], "username": row[7]} })
        
        return response

    @staticmethod
    def find_ten_latest_topics_by_user_id(user_id):
        stmt = text("SELECT t.id, t.name, t.date_created"
                    " FROM topic t"
                    " WHERE t.account_id = :user_id"
                    " ORDER BY t.date_created DESC"
                    " LIMIT 10").params(user_id = user_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({ "id": row[0], "name": row[1], "date_created": row[2] })
        
        return response
