from zapros import *
import unittest

class TestRequests(unittest.TestCase):
    @classmethod 
    def setUpClass(cls):
        cls.db = DB(path=":memory:")
        cursor = cls.db.newCursor()
        cls.db.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS "Goods" (
                "ID"	INTEGER,
                "Name"	TEXT NOT NULL,
                "Quantity"	INTEGER NOT NULL,
                "СategoryID"	INTEGER,
                "Description"	TEXT,
                "PriceID"	INTEGER UNIQUE,
                PRIMARY KEY("ID"),
                FOREIGN KEY("СategoryID") REFERENCES "Categories"("ID"),
                FOREIGN KEY("PriceID") REFERENCES "Prices"("ID")
        );
        CREATE TABLE IF NOT EXISTS "Categories" (
                "ID"	INTEGER,
                "Name"	TEXT NOT NULL UNIQUE,
                "Description"	TEXT,
                PRIMARY KEY("ID")
        );
        CREATE TABLE IF NOT EXISTS "Prices" (
                "ID"	INTEGER,
                "Price"	INTEGER NOT NULL,
                "GoodID"	INTEGER,
                "StartDate"	TEXT NOT NULL,
                "EndDate"	TEXT NOT NULL,
                PRIMARY KEY("ID"),
                FOREIGN KEY("GoodID") REFERENCES "Goods"("ID")
        );
        CREATE TABLE IF NOT EXISTS "Customers" (
                "ID"	INTEGER,
                "Surname"	TEXT NOT NULL,
                "Name"	TEXT NOT NULL,
                "Patronymic"	TEXT,
                "PhoneNumber"	TEXT UNIQUE,
                "E-mail"	BLOB UNIQUE,
                "RegistrationDate"	TEXT NOT NULL,
                "Login"	TEXT UNIQUE,
                "PasswordHash"	INTEGER NOT NULL,
                "BankCardNumber"	TEXT,
                "PassportSeriesAndNumber"	TEXT UNIQUE,
                "PassportDateOfIssue"	TEXT,
                "PassportWhoIssued"	TEXT,
                "ShopCardNumber"	INTEGER UNIQUE,
                "ShopCardDateOfIssue"	TEXT,
                "ShopCardBuyAmount"	INTEGER,
                "Address"	TEXT,
                "Age"	INTEGER,
                PRIMARY KEY("ID")
        );
        CREATE TABLE IF NOT EXISTS "Orders" (
                "NumberOfOrder"	INTEGER,
                "Quantity"	INTEGER NOT NULL,
                "PriceID"	INTEGER,
                "CustomerID"	INTEGER,
                "Date"	TEXT NOT NULL,
                "Status"	TEXT,
                FOREIGN KEY("CustomerID") REFERENCES "Customers"("ID"),
                FOREIGN KEY("PriceID") REFERENCES "Prices"("ID")
        );
        ''')
        cls.db.connection.commit()

    @classmethod 
    def tearDownClass(cls):
        cls.db.connection.close()

    def setUp(self):
        self.db.newCursor()
        self.db.cursor.execute("SELECT DATE('now')")
        cur=self.db.cursor.fetchall()
        cur=cur[0][0]
        self.db.cursor.executescript('''
        INSERT INTO "Goods" VALUES (1,'Флешка №1',30,1,'16 GB Цвет: синий',1);
        INSERT INTO "Goods" VALUES (2,'Клавиатура №1',60,2,'Цвет: чёрный',2);
        INSERT INTO "Goods" VALUES (3,'Телевизор №1',20,3,'Цвет: чёрный',3);
        INSERT INTO "Categories" VALUES (1,'Флешки','Различные флешки');
        INSERT INTO "Categories" VALUES (2,'Клавиатуры','Клавиатуры на ваш выбор');
        INSERT INTO "Categories" VALUES (3,'Телевизоры','Телевизоры');''')
        self.db.cursor.execute("INSERT INTO 'Prices' VALUES (1,1000,1,'2021-11-13',:cur_date);",{"cur_date":cur})
        self.db.cursor.execute("INSERT INTO 'Prices' VALUES (2,2000,2,'2021-11-13',:cur_date);",{"cur_date":cur})
        self.db.cursor.execute("INSERT INTO 'Prices' VALUES (3,20000,3,'2021-11-13',:cur_date);",{"cur_date":cur})
        self.db.cursor.executescript('''INSERT INTO "Prices" VALUES (4,500,1,'2018-01-01','2021-11-12');
        INSERT INTO "Prices" VALUES (5,1500,2,'2018-01-01','2021-11-12');
        INSERT INTO "Customers" VALUES (1,'Шомполов','Максим','Андреевич','81234567890','qwerty@google.com','2021-10-11','qwery',12345,'1234567890123456','12 34 567890','2021-11-13','ГУ МВД ПО Г. МОСКВЕ',123456789,'2021-11-13',5000,'город Москва, Балаклавский проспект, дом 6А',21);
        INSERT INTO "Customers" VALUES (2,'Иванов','Иван','Иванович','89635274107','abcd@yandex.ru','2021-11-14','abcd',54321,'3216549870789456','98 87 455612','2004-01-01','ГУ МВД ПО Г. МОСКВЕ',345343455,'2021-10-20',9000,'город Москва, Балаклавский проспект, дом 6А',40);
        INSERT INTO "Customers" VALUES (3,'Петров','Пётр','Петрович','83216543215','asdfhjas@mail.ru','2021-11-11','dcba',56484,'5465468421465845','21 21 342764','2021-11-14','ГУ МВД ПО Г. МОСКВЕ',567765788,'2021-09-09',15000,'город Москва, Балаклавский проспект, дом 6А',35);
        INSERT INTO "Orders" VALUES (1,2,1,1,'2021-11-13','ReadyToByDelivered');
        INSERT INTO "Orders" VALUES (2,1,2,1,'2021-11-12','Delivered');
        INSERT INTO "Orders" VALUES (1,3,2,2,'2021-11-13','ReadyToByDelivered');
        INSERT INTO "Orders" VALUES (3,4,3,3,'2021-11-13','ReadyToByDelivered');
        ''')
        self.db.connection.commit()

    def tearDown(self):
        self.db.cursor.executescript('''
        DELETE FROM Goods;
        DELETE FROM Categories;
        DELETE FROM Prices;
        DELETE FROM Customers;
        DELETE FROM Orders;
        ''')

    def test_ReadyOrders_Some(self):
        expectedResult=[(1, 1, 1000, 2, 1), (1, 2, 2000, 3, 2), (3, 3, 20000, 4, 3)]
        self.assertEqual(self.db.ReadyOrders(),expectedResult,'Ready orders ids are 1 and 3')

    def test_ReadyOrders_None(self):
        self.db.newCursor()
        self.db.cursor.execute("UPDATE Orders set Status='Delivered'")
        self.db.connection.commit()
        self.assertEqual(self.db.ReadyOrders(),[],'There is no ready orders')

    def test_UpdatePrices_None(self):
        self.db.UpdatePrices()
        self.db.cursor.execute("SELECT StartDate,EndDate FROM Prices WHERE Prices.ID=(SELECT PriceID FROM Goods where Goods.id=Prices.GoodID)")
        dates=self.db.cursor.fetchall()
        self.db.cursor.execute("SELECT DATE('now')")
        cur=self.db.cursor.fetchall()
        k=0
        for i in dates:
            if not(i[0]<=cur[0][0]<=i[1]):
                k+=1
                break
        self.assertEqual(k,0,'Not all prices are relevant')

    def test_UpdatePrices_Some(self):
        self.db.cursor.execute("UPDATE Goods SET PriceID=4 WHERE ID=1")
        self.db.cursor.execute("UPDATE Goods SET PriceID=5 WHERE ID=2")
        self.db.UpdatePrices()
        self.db.cursor.execute("SELECT StartDate,EndDate FROM Prices WHERE Prices.ID=(SELECT PriceID FROM Goods where Goods.id=Prices.GoodID)")
        dates=self.db.cursor.fetchall()
        
        self.db.cursor.execute("SELECT DATE('now')")
        cur=self.db.cursor.fetchall()
        k=0
        for i in dates:
            if not(i[0]<=cur[0][0]<=i[1]):
                k+=1
                break
        self.assertEqual(k,0,'Not all prices are relevant')

    def test_UpdatePrices_No_New_Price(self):
        self.db.cursor.execute("UPDATE Prices set EndDate='2021-12-01' WHERE Prices.id=3;")
        self.db.UpdatePrices()
        self.db.cursor.execute("SELECT PriceID FROM Goods WHERE Goods.ID=3;")
        res=self.db.cursor.fetchall()
        
        self.assertEqual(res[0][0],None,'Wrong for no price')

    def test_CategoryGoods_Some(self):
        self.db.cursor.execute("SELECT DATE('now')")
        cur=self.db.cursor.fetchall()
        expectedResult=[('Клавиатура №1', 60, 'Цвет: чёрный', 2000, cur[0][0])]
        self.assertEqual(self.db.CategoryGoods(2),expectedResult,'Not correct goods for Category 2')

    def test_CategoryGoods_No_Goods(self):
        self.assertEqual(self.db.CategoryGoods(4),[],'Not correct work for no goods category')

    def test_CategoryGoods_No_Category(self):
        self.assertEqual(self.db.CategoryGoods(5),[],'Not correct work for no such category')

if __name__=='__main__':
    unittest.main()
        

    
