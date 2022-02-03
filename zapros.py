import sqlite3

class DB:
    def __init__(self,path):
        self.connection = sqlite3.connect(path)

    def newCursor(self):
        self.cursor = self.connection.cursor()
    
    #1
    def ReadyOrders(self):
        self.cursor.execute(
            '''
            SELECT 
                NumberOfOrder,
                (SELECT GoodID FROM Prices WHERE ID=PriceID) AS GoodID,
                (SELECT Price FROM Prices WHERE ID=PriceID) AS Price,
                Quantity,
                CustomerID
                FROM Orders WHERE Status = 'ReadyToByDelivered';
            '''
        )
        return self.cursor.fetchall()

    #2
    def UpdatePrices(self):
        self.cursor.execute(
            '''
            UPDATE Goods SET PriceID=(SELECT ID FROM Prices WHERE GoodID=Goods.ID and EndDate>=(SELECT DATE('now')) and StartDate<=(SELECT DATE('now')))
            WHERE (SELECT EndDate FROM Prices WHERE Goods.PriceID=Prices.ID)<(SELECT DATE('now'));
            '''
        )

    #3
    def CategoryGoods(self,category):
        self.cursor.execute(
            '''
            SELECT
                Name,
                Quantity, 
                Description,
                (SELECT Price FROM Prices WHERE Prices.ID=PriceID)AS Price,
                (SELECT EndDate FROM Prices WHERE Prices.ID=PriceID)AS EndDate
                FROM Goods WHERE Goods.СategoryID=?;
            ''',(category,)
        )
        return self.cursor.fetchall()

path='DataBase.db'

db=DB(path)
db.newCursor()
#print(db.ReadyOrders())
#print(db.CategoryGoods(2))
#DB.UpdatePrices()
'''db._connection'.commit()
db._connection'.close()'''

