import random
import time
from decimal import Decimal

import pymysql

con = pymysql.connect(host='192.168.31.229', user='BigCat',
                      password='0000', database='exchange_service')

def getCrypto():
    cur = con.cursor()
    array = []
    cur.execute(f"SELECT price, amount FROM exchange_service.order_books where stock_id = {1} order by price")
    fetch = cur.fetchall()
    for order in fetch:
        print(order)
        i = 0
        while i < order[1]:
            array.append(str(order[0]))
            i += 1
            if len(array) == 100:
                print('work')
                print(array)
                return array

def closeCorder(price):
    cur = con.cursor()
    cur.execute(f"SELECT price, amount FROM exchange_service.order_books where id = {id} and stock_id = {1}")

with con:
    getCrypto()

# multiplier = Decimal(random.uniform(0.95, 1.05))
# new_price = fetch * multiplier
# cur.execute(f"UPDATE order_books SET price = {new_price} WHERE id = {id}")
# cur.execute(f"SELECT price FROM exchange_service.order_books where id = {id}")
# fetch = cur.fetchall()[0][0]