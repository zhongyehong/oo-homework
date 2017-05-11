from model import *


class SystemUser(object):
    def __init__(self,user):
        self.obj = user
        self.collection = []
        coll = Collection.query.filter_by(userid = self.obj.id)
        if (coll != None):
            for one in coll:
                self.collection.append(one.bookid)
        self.orderform = []
        order = OrderForm.query.filter_by(userid = self.obj.id)
        if (order != None):
            for one in order:
                self.orderform.append(one.id)

    @staticmethod
    def auth(username,password):
        user = User.query.filter_by(username = username).first()
        if (user == None):
            return False
        if user.password == password:
            return True
        else:
            return False
    
    def pay(self, tuser,amount):
        if(self.obj.money < amount):
            return False
        self.obj.money = self.obj.money - amount
        tuser.money = tuser.money + amount
        db.session.flush()
        db.session.commit()
        return True
    
    @staticmethod
    def getAllOrderForm():
        orderforms = []
        allorderforms = OrderForm.query.all()
        for order in allorderforms:
            orderforminfo = {}
            orderforminfo['id'] = order.id
            orderforminfo['bookid'] = order.bookid
            orderforminfo['userid'] = order.userid
            book = Book.query.filter_by(id = order.bookid).first()
            user = User.query.filter_by(id = order.userid).first()
            orderforminfo['bookname'] = book.bookname
            orderforminfo['username'] = user.username 
            orderforminfo['price'] = book.price
            orderforminfo['address'] = order.address
            orderforminfo['status'] = order.status
            orderforms.append(orderforminfo)
        return orderforms

    def getCollection(self):
        collbooks = []
        for bookid in self.collection:
            book = Book.query.filter_by(id = bookid).first()
            bookinfo = {}
            bookinfo['id'] = bookid
            bookinfo['number'] = book.number
            bookinfo['description'] = book.description
            bookinfo['bookname'] = book.bookname
            bookinfo['price'] = book.price
            collbooks.append(bookinfo)
        return collbooks
    
    def collect(self,bookid):
        collect = Collection(self.obj.id,bookid)
        db.session.add(collect)
        db.session.commit()
        self.collection.append(bookid)
        return True

    def bid(self,stockformid,curprice):
        stockform = StockOrderForm.query.filter_by(id=stockformid).first()
        if curprice >= stockform.curprice:
            return False
        else:
            stockform.curprice = curprice
            stockform.bidder = self.obj.id
            db.session.commit()
            return True

    def acceptStockOrderForm(self,stockformid):
        stockform = StockOrderForm.query.filter_by(id=stockformid).first()
        stockform.status = "closed"
        book = Book.query.filter_by(id=stockform.bookid).first()
        book.number = book.number + stockform.number
        supplier = User.query.filter_by(id=stockform.bidder).first()
        self.pay(supplier,stockform.curprice)
        db.session.commit()
        return True
        
    def createOrderForm(self, bookid, address):
        orderform = OrderForm(self.obj.id, bookid, address, 'waiting for pay')
        db.session.add(orderform)
        db.session.commit()
        self.orderform.append(orderform.id)
        return True

    def createStockOrderForm(self, bookid, number, initprice):
        stockorderform = StockOrderForm(bookid, number, initprice)
        db.session.add(stockorderform)
        db.session.commit()
        return True
    
    @staticmethod
    def getAllStockOrderForm():
        stockorderforms = []
        allstockorderforms = StockOrderForm.query.all()
        for order in allstockorderforms:
            orderforminfo = {}
            orderforminfo['id'] = order.id
            orderforminfo['bookid'] = order.bookid
            orderforminfo['bidderid'] = order.bidder
            book = Book.query.filter_by(id = order.bookid).first()
            user = User.query.filter_by(id = order.bidder).first()
            orderforminfo['bookname'] = book.bookname
            if order.bidder == 0:
                orderforminfo['biddername'] = ""
            else:
                orderforminfo['biddername'] = user.username
            orderforminfo['curprice'] = order.curprice
            orderforminfo['status'] = order.status
            stockorderforms.append(orderforminfo)
        return stockorderforms

    def getStockOrderForm(self):
        stockorderforms = []
        allstockorderforms = StockOrderForm.query.filter_by(bidder = self.obj.id)
        for order in allstockorderforms:
            orderforminfo = {}
            orderforminfo['id'] = order.id
            orderforminfo['bookid'] = order.bookid
            orderforminfo['bidderid'] = order.bidder
            book = Book.query.filter_by(id = order.bookid).first()
            user = User.query.filter_by(id = order.bidder).first()
            orderforminfo['bookname'] = book.bookname
            orderforminfo['biddername'] = user.username
            orderforminfo['curprice'] = order.curprice
            orderforminfo['status'] = order.status
            stockorderforms.append(orderforminfo)
        return stockorderforms

    def payforOrderForm(self, orderformid, shopkeeper):
        orderform = OrderForm.query.filter_by(id = orderformid).first()
        bookid = orderform.bookid
        book = Book.query.filter_by(id = bookid).first()
        price = book.price
        if orderform.status == 'paid':
            return True
        if self.pay(shopkeeper.obj, price) == True:
            orderform.status = 'paid'
            book.number = book.number-1
            db.session.commit()
            return True
        else:
            return False
    
    def getOrderForm(self):
        orderforms = []
        for orderformid in self.orderform:
            order = OrderForm.query.filter_by(id = orderformid).first()
            orderforminfo = {}
            orderforminfo['id'] = orderformid
            orderforminfo['bookid'] = order.bookid
            book = Book.query.filter_by(id = order.bookid).first()
            orderforminfo['bookname'] = book.bookname
            orderforminfo['price'] = book.price
            orderforminfo['address'] = order.address
            orderforminfo['status'] = order.status
            orderforms.append(orderforminfo)
        return orderforms

