from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

import hashlib
from datetime import datetime

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    registration_date = db.Column(db.DateTime, nullable=False)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200), nullable=False)
    total_orders = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Integer)

    patronymic = db.Column(db.String(80))
    bank_card_number = db.Column(db.String(80))
    passport_series_and_number = db.Column(db.String(80), unique=True)
    passport_date_of_issue = db.Column(db.DateTime)
    passport_who_issued = db.Column(db.String(80))
    shop_card_number = db.Column(db.Integer)
    shop_card_date_of_issue = db.Column(db.DateTime)
    shop_card_buy_amount = db.Column(db.Integer)
    address = db.Column(db.String(80))
    age = db.Column(db.Integer)

    def hash_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()

    def validate(self, password):
        return self.password == hashlib.md5(password.encode('utf8')).hexdigest()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    review = db.Column(db.String(200))

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    price_id = db.Column(db.Integer, db.ForeignKey('prices.id'))
    price = db.relationship('Prices', backref=db.backref('good', lazy=False))
    photo_link = db.Column(db.String(80))
    colour = db.Column(db.String(80))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Categories', backref=db.backref('goods', lazy=False))

    def link(self):
        return '/product?good_id='+str(self.id)
    

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_order = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    good = db.relationship('Goods', backref=db.backref('orders', lazy=False))
    price_id = db.Column(db.Integer, db.ForeignKey('prices.id'))
    price = db.relationship('Prices', backref=db.backref('orders', lazy=False))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customers', backref=db.backref('orders', lazy=False))
    date = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(80), nullable=False)

class Shopping_cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customers', backref=db.backref('shopping_cart', lazy=False))
    quantity = db.Column(db.Integer, nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    good = db.relationship('Goods', backref=db.backref('shopping_cart', lazy=False))

class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    

#db.create_all()
'''x=Feedback(name = '1', review = '2')
db.session.add(x)
db.session.commit()'''
#db.close()



'''category1 = Categories(name = 'Keyboards', description = 'Best keyboards')
good1 = Goods(name = 'Keyboard 1', quantity = 5, category_id = 1, description = 'Keyboard 1', price_id = 0)
price1 = Prices(price = 2000, start_date = datetime.now(), end_date = datetime.now())

db.session.add(category1)
db.session.add(good1)
db.session.add(price1)

db.session.commit()'''

#print(Feedback.query.all()[0].name)


