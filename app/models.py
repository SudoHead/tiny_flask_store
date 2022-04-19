from select import select
from . import db


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

    service_fee_id = db.Column(db.Integer, 
        db.ForeignKey('service_fee.id'), nullable = False)
    service_fee = db.relationship('ServiceFee', backref='event', lazy='select')

    def __init__(self, id, name, service_fee_id):
        self.id = id
        self.name = name
        self.service_fee_id = service_fee_id

    def __repr__(self):
        return f'<Event #{self.id} - {self.name}>'


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable = False)
    name = db.Column(db.String)
    service_fee_id = db.Column(db.Integer, 
        db.ForeignKey('service_fee.id'), nullable = True)

    service_fee = db.relationship('ServiceFee', backref='product', lazy='select')
    event = db.relationship('Event', backref='product_event', lazy='select')

    def __init__(self, id, event_id, name, service_fee_id):
        self.id = id
        self.name = name
        self.event_id = event_id
        self.service_fee_id = service_fee_id

    def __repr__(self):
        return f'<Product #{self.id} - {self.name}>'


class ServiceFee(db.Model):
    __tablename__ = 'service_fee'

    id = db.Column(db.Integer, primary_key = True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    currency = db.relationship('Currency', backref='service_fee', lazy='select')
    amount = db.Column(db.Numeric(10, 2))

    def __init__(self, id, currency_id, amount):
        self.id = id
        self.currency_id = currency_id
        self.amount = amount

    def __repr__(self):
        return f'<ServiceFee #{self.id} - {self.amount}>'


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key = True)
    iso = db.Column(db.CHAR(3))

    def __init__(self, id, iso):
        self.id = id
        self.iso = iso

    def __repr__(self):
        return f'<Currency #{self.id} - {self.iso}>'
