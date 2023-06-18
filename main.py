import random
import time
from decimal import Decimal

import pymysql

con = pymysql.connect(host='192.168.31.229', user='BigCat',
                      password='0000', database='exchange_service')

def getCrypto():
    cur = con.cursor()
    array = []
    try:
        cur.execute(f"SELECT price, amount FROM exchange_service.order_books where stock_id = {1} and operation = 'buy' order by price")
        fetch = cur.fetchall()
        for order in fetch:
            i = 0
            while i < order[1]:
                array.append(str(order[0]))
                i += 1
                if len(array) == 100:
                    return array
    finally:
        cur.close()

def closeOrder(price):
    cur = con.cursor()
    try:
        cur.execute(f"SELECT amount FROM exchange_service.order_books where stock_id = {1} and operation = 'buy' and price = {price} order by price LIMIT 1")
        amount = cur.fetchall()[0][0]
        print(amount)
        if amount == 1:
            cur.execute(f"DELETE FROM exchange_service.order_books where stock_id = {1} and price = {price} and amount = 1")
        else:
            cur.execute(f"Update exchange_service.order_books SET amount = {amount - 1} where stock_id = 1 and price = {price}")
        cur.fetchall()
        con.commit()
    finally:
        cur.close()

with con:
    getCrypto()
    closeOrder(363.61)