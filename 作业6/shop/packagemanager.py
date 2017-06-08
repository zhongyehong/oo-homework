from model import db,Book,Package

class PackageManager():
    

    @staticmethod
    def str2list(bookids):
        return bookids.split(',')
    
    @staticmethod
    def list2str(bookids):
        return ','.join(bookids)

    @staticmethod
    def createPackage(packagename, bookids, price, description):
        package = Package(packagename, PackageManager.list2str(bookids), price, description)
        db.session.add(package)
        db.session.commit()
        return True

    @staticmethod
    def deletePackage(packageid):
        package = Package.query.filter_by(id=packageid).first()
        db.session.delete(package)
        db.session.commit()

    '''
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
    '''
    @staticmethod
    def getPackageInfo():
        packages = Package.query.all()
        packagesinfo = []
        for package in packages:
            packagesinfo.append(PackageManager.getPackageInfoById(package.id))
        return packagesinfo

    @staticmethod
    def getPackageInfoById(packageid):
        package = Package.query.filter_by(id = packageid).first()
        bookids = PackageManager.str2list(package.books)
        booksinfo = []
        for bookid in bookids:
            booksinfo.append(
                    {
                        'id':bookid,
                        'bookname':Book.query.filter_by(id=bookid).first().bookname
                    })
        packageinfo = {
               'id': package.id,
               'packagename': package.packagename,
               'booksinfo': booksinfo,
               'price': package.price,
               'description': package.description
               }
        return packageinfo

