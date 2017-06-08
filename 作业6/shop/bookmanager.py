from model import db,Book

class BookManager():
    
    @staticmethod
    def createBook(bookname, price, number, description):
        book = Book(bookname,price,number,description)
        db.session.add(book)
        db.session.commit()
        return True


    @staticmethod
    def editBookInfo(bookid, bookname, price, number, description):
        book = Book.query.filter_by(id = bookid).first()
        book.bookname = bookname
        book.price = price
        book.number = number
        book.description = description
        db.session.commit()
        return True

    @staticmethod
    def changeNumber(bookid,delta):
        book = Book.query.filter_by(id = bookid).first()
        book.number = book.number + delta
        db.session.commit()
        return True

    @staticmethod
    def getBookInfo():
        books = Book.query.all()
        booksinfo = []
        for book in books:
            bookinfo = {
                    'id': book.id,
                    'bookname': book.bookname,
                    'price': book.price,
                    'number': book.number,
                    'description': book.description,
                    'bookerid':book.bookerid,
                    'trueprice':float(book.price)*float(book.discount)/10,
                    'discount':book.discount
                    }
            booksinfo.append(bookinfo)
        return booksinfo

    @staticmethod
    def getBookInfoById(bookid):
        book = Book.query.filter_by(id = bookid).first()
        bookinfo = {
               'id': book.id,
               'bookname': book.bookname,
               'price': book.price,
               'number': book.number,
               'description': book.description,
               'bookerid':book.bookerid,
               'trueprice':float(book.price)*float(book.discount)/10,
               'discount':book.discount
               }
        return bookinfo

