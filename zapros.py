import sqlite3
conn = sqlite3.connect('DataBase.db')
cursor = conn.cursor()

#1

def ReadyOrders():
    cursor.execute(
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
    print(cursor.fetchall())

#2
def UpdatePrices():
    cursor.execute(
        '''
        UPDATE Goods SET PriceID=(SELECT ID FROM Prices WHERE GoodID=Goods.ID and EndDate>=(SELECT DATE('now')) and StartDate<=(SELECT DATE('now')))
        WHERE (SELECT EndDate FROM Prices WHERE Goods.PriceID=Prices.ID)<(SELECT DATE('now'));
        '''
    )

#3

def CategoryGoods():
    cursor.execute(
        '''
        SELECT
            Name,
            Quantity, 
            Description,
            (SELECT Price FROM Prices WHERE Prices.ID=PriceID)AS Price,
            (SELECT EndDate FROM Prices WHERE Prices.ID=PriceID)AS EndDate
            FROM Goods WHERE Goods.СategoryID=2;
        '''
    )
    print(cursor.fetchall())

#4
def CategoryInformation():
    cursor.execute('SELECT name, Description FROM Categories WHERE ID=1')
    print(cursor.fetchall())

#5
def UpdateOrder():
    cursor.execute("UPDATE Orders SET Status='Delivered' WHERE NumberOfOrder=1;")

#6
def ReduceQuantity():
    cursor.execute("UPDATE Goods SET Quantity=Quantity-5 WHERE ID = 1;")


'''ReadyOrders()
CategoryGoods()
CategoryInformation()'''
#UpdatePrices()
#UpdateOrder()
ReduceQuantity()
conn.commit()
conn.close()

