from application import db
from application.models import Base

class Category(Base):

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    topics = db.relationship("Topic", backref='category_topic', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description