from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///mydb.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    usertype = db.Column(db.String(10))
    password = db.Column(db.String(100))
    money = db.Column(db.Float)
    

    def __init__(self, username, password, money=1000, usertype = "customer"):
        self.username = username
        self.password = password
        self.money = money
        self.usertype = usertype

    def __repr__(self):
        return '<User %r>' % (self.username)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(100))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    description = db.Column(db.String(100))
    
    def __init__(self, bookname, price = 20, number = 100, description = "a book"):
        self.bookname = bookname
        self.price = price
        self.number = number
        self.description = description

    def __repr__(self):
        return '<Book %r>' % (self.bookname)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    bookid = db.Column(db.Integer)

    def __init__(self, userid, bookid):
        self.userid = userid
        self.bookid = bookid

class OrderForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    bookid = db.Column(db.Integer)
    address = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, userid, bookid, address, status="processing"):
        self.userid = userid
        self.bookid = bookid
        self.address =  address
        self.status = status

class StockOrderForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer)
    number = db.Column(db.Integer)
    bidder = db.Column(db.Integer)
    curprice = db.Column(db.Float)
    status = db.Column(db.String(100))

    def __init__(self,  bookid, number, curprice, bidder = 0, status = "bidding"):
        self.bookid = bookid
        self.number = number
        self.curprice = curprice
        self.bidder = bidder
        self.status = status
