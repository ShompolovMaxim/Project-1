from ORM import *

from datetime import datetime

db.create_all()
good1=Goods(name='Флешка №1',quantity=90,photo_link='Флешка№1.jpg',colour='синий')
good2=Goods(name='Флешка №2',quantity=90,photo_link='Флешка№1.jpg',colour='красный')
good3=Goods(name='Флешка №3',quantity=90,photo_link='Флешка№1.jpg',colour='зелёный')
good4=Goods(name='Флешка №4',quantity=90,photo_link='Флешка№1.jpg',colour='чёрный')
price1=Prices(price=3000,start_date=datetime.now(),end_date=datetime.now())
price2=Prices(price=5000,start_date=datetime.now(),end_date=datetime.now())
price3=Prices(price=4000,start_date=datetime.now(),end_date=datetime.now())
price4=Prices(price=1000,start_date=datetime.now(),end_date=datetime.now())
good1.price=price1
good2.price=price2
good3.price=price3
good4.price=price4
db.session.add(good1)
db.session.add(good2)
db.session.add(good3)
db.session.add(good4)
db.session.add(price1)
db.session.add(price2)
db.session.add(price3)
db.session.add(price4)
db.session.commit()
