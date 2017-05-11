#!/usr/bin/python3

import json, os, sys

from flask import *
from user import *
from bookmanager import *

app = Flask(__name__)

global userlist

@app.route("/", methods = ['GET'])
def home():
    return redirect("/login/")

@app.route("/login/", methods = ['GET'])
def login():
    if 'username' in session:
        if session['usertype'] == 'supplier':
            return redirect('/stockorderforms/')
        else:
            return redirect('/books/')
    else:
        return render_template('login.html')

@app.route("/trylogin/", methods = ['POST'])
def trylogin():
    username = request.form['username']
    password = request.form['password']
    res = SystemUser.auth(username, password)
    if res == True:
        session['username'] = username
        session['usertype'] = userlist[username].obj.usertype
        session['money'] = userlist[username].obj.money
        return redirect("/books/")
    else:
        return redirect("/login/")

@app.route("/logout/", methods = ['GET'])
def logout():
    session.pop('username', None)
    session.pop('money', None)
    session.pop('usertype', None)
    return redirect("/login/")

@app.route("/message/<message>/", methods = ['GET'])
def messaege(message):
    return render_template('message.html', message = message)

@app.route("/books/", methods = ['GET'])
def books():
    global userlist
    books = BookManager.getBookInfo()
    collectioninfos = userlist[session['username']].getCollection()
    collections = []
    for collectioninfo in collectioninfos:
        collections.append(collectioninfo['id'])
    return render_template('books.html', books = books, collections = collections, session = session)

@app.route("/addbook/", methods = ['GET'])
def addbook():
    return render_template('addbook.html', session = session)

@app.route("/createbook/", methods = ['POST'])
def createbook():
    bookname = request.form['bookname']
    price = float(request.form['price'])
    number = int(request.form['number'])
    description = request.form['description']
    BookManager.createBook(bookname, price, number, description)
    return redirect('/books/')

@app.route("/addstockform/<bookid>/", methods = ['GET'])
def addstockform(bookid):
    bookinfo = BookManager.getBookInfoById(bookid)
    return render_template('addstockform.html', session = session, bookinfo = bookinfo)

@app.route("/acceptstockform/<stockformid>/", methods = ['GET'])
def acceptstockform(stockformid):
    userlist[session['username']].acceptStockOrderForm(stockformid)
    session['money'] = userlist[session['username']].obj.money
    return redirect('/allstockorderforms/')

@app.route("/createstockform/<bookid>/", methods = ['POST'])
def createstockform(bookid):
    number = int(request.form['number'])
    initprice = float(request.form['initprice'])
    userlist[session['username']].createStockOrderForm(bookid,number,initprice)
    return redirect('/allstockorderforms/')


@app.route("/collections/", methods = ['GET'])
def collections():
    global userlist
    collections = userlist[session['username']].getCollection()
    return render_template('collections.html', collections = collections, session = session)

@app.route("/orderforms/", methods = ['GET'])
def orderforms():
    global userlist
    orderforms = userlist[session['username']].getOrderForm()
    return render_template('orderforms.html', orderforms = orderforms, session = session)

@app.route("/allorderforms/", methods = ['GET'])
def allorderforms():
    orderforms = SystemUser.getAllOrderForm()
    return render_template('orderforms.html', orderforms = orderforms, session = session)

@app.route("/stockorderforms/", methods = ['GET'])
def stockorderforms():
    global userlist
    orderforms = userlist[session['username']].getStockOrderForm()
    return render_template('stockorderforms.html', orderforms = orderforms, session = session)

@app.route("/allstockorderforms/", methods = ['GET'])
def allstockorderforms():
    orderforms = SystemUser.getAllStockOrderForm()
    return render_template('stockorderforms.html', orderforms = orderforms, session = session)

@app.route("/collect/<bookid>/", methods = ['GET'])
def collect(bookid):
    global userlist
    userlist[session['username']].collect(int(bookid))
    return redirect("/books/")

@app.route("/buy/<bookid>/", methods = ['GET'])
def buy(bookid):
    global userlist
    userlist[session['username']].createOrderForm(int(bookid),'pku')
    return redirect("/orderforms/")

@app.route("/bid/<stockformid>/", methods = ['POST'])
def bid(stockformid):
    global userlist
    curprice = float(request.form['curprice'])
    res = userlist[session['username']].bid(stockformid,curprice)
    if res == True:
        return render_template("message.html", message="出价成功", session = session)
    else:    
        return render_template("message.html", message="出价失败，出价必须低于当前价格", session = session)

@app.route("/pay/<orderformid>/", methods = ['GET'])
def pay(orderformid):
    global userlist
    res = userlist[session['username']].payforOrderForm(int(orderformid),userlist['shopkeeper'])
    session['money'] = userlist[session['username']].obj.money
    if res == True:
        return render_template("message.html", message = "付款成功")
    else:
        return render_template("message.html", message = "余额不足，付款失败")


if __name__ == '__main__':
    try:
        User.query.all()
    except:
        db.create_all()
        customer = User('customer','customer',1000,"customer")
        customer2 = User('customer2','customer2',3000,"customer")
        shopkeeper = User('shopkeeper','shopkeeper',10000, "shopkeeper")
        supplier = User('supplier', 'supplier', 5000, "supplier")
        db.session.add(customer)
        db.session.add(customer2)
        db.session.add(shopkeeper)
        db.session.add(supplier)
        db.session.commit()
        oo = Book("oo", 50, 100, "oo教材")
        thinkuml = Book("大象", 100, 30, "thinking in uml")
        python = Book("python设计原理", 30, 5, "python教材")
        db.session.add(oo)
        db.session.add(thinkuml)
        db.session.add(python)
        db.session.commit()

    try: 
        secret_key_file = open('secret_key.txt')
        app.secret_key =secret_key_file.read()
        secret_key_file.close()
    except:
        from base64 import b64encode
        from os import urandom
        secret_key = urandom(24)
        secret_key = b64encode(secret_key).decode('utf-8')
        app.secret_key = secret_key
        secret_key_file = open('secret_key.txt', 'w')
        secret_key_file.write(secret_key)
        secret_key_file.close()
    os.environ['APP_KEY'] = app.secret_key

    userlist = {}
    users = User.query.all()
    for user in users:
        userlist[user.username] = SystemUser(user)

    
    app.run(host = "0.0.0.0", port = 9555, threaded=True, debug=True)

