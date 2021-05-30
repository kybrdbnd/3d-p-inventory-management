import enum
import random
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from inventory_management import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return self.name


class FilamentCategory(db.Model):
    __tablename__ = 'filament_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    filaments = db.relationship('Filament', backref='filament_category', lazy=True)

    def __repr__(self):
        return self.name


class Filament(db.Model):
    __tablename__ = 'filaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    filament_category_id = db.Column(db.Integer, db.ForeignKey('filament_categories.id'))
    price_per_gram = db.Column(db.Integer)

    def __repr__(self):
        return self.name


class Figure(db.Model):
    __tablename__ = 'figures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    count = db.Column(db.Integer, default=0)
    extras = db.Column(MutableDict.as_mutable(JSONB))
    items = db.relationship('Item', backref='figure', lazy=True)

    def __repr__(self):
        return self.name


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    ph_no = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return self.email


class ItemStatus(enum.Enum):
    not_started = 'not_started'
    in_progress = 'in_progress'
    delivered = 'delivered'


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_no = db.Column(db.Integer)
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.not_started, nullable=False)
    figure_id = db.Column(db.Integer, db.ForeignKey('figures.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.item_no = random.randint(100, 4000)

    def __repr__(self):
        return str(self.item_no)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    feedback = db.Column(db.String())
    address = db.Column(db.Text())
    created_on = db.Column(db.DateTime())
    delivered_on = db.Column(db.DateTime())
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    items = db.relationship('Item', backref='order', lazy=True)

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.order_id = random.randint(40, 20000)

    def __repr__(self):
        return str(self.order_id)


class Query(db.Model):
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer)
    name = db.Column(db.String())
    comment = db.Column(db.Text())
    created_on = db.Column(db.DateTime())
    extras = db.Column(MutableDict.as_mutable(JSONB))

    def __init__(self, **kwargs):
        super(Query, self).__init__(**kwargs)
        self.query_id = random.randint(40, 20000)
        self.created_on = datetime.now()

    def __repr__(self):
        return str(self.query_id)


if __name__ == '__main__':
    db.create_all()
