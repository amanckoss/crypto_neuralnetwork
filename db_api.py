import decimal
import random
import pymysql

con = pymysql.connect(host='192.168.31.229', user='BigCat',
                      password='0000', database='exchange_service')


def change_crypto_type_course(crypto_type):
    rand_num = decimal.Decimal(random.uniform(-0.03, 0.03))
    print('buy')
    change_market_course(crypto_type, 'buy', rand_num)
    print('sell')
    change_market_course(crypto_type, 'sell', rand_num)
    con.commit()


def change_market_course(crypto_type, operation, rand_numb):
    cur = con.cursor()
    cur.execute(f"SELECT id, price FROM exchange_service.order_books where stock_id = {crypto_type} and operation = '{operation}'")
    crypto = cur.fetchall()
    print(crypto)
    for cr in crypto:
        new_price = cr[1] + cr[1] * rand_numb
        cur.execute(
            f"Update exchange_service.order_books SET price = {new_price} where id ={cr[0]}")
    cur.fetchall()
    cur.execute(f"SELECT id, price FROM exchange_service.order_books where stock_id = {crypto_type}")
    new_crypto = cur.fetchall()
    print(new_crypto)


def get_orders(operation):
    cur = con.cursor()
    array = []
    try:
        cur.execute(
            f"SELECT price, amount FROM exchange_service.order_books where stock_id = {1} and operation = '{operation}' order by price")
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


def close_order(price, operation):
    cur = con.cursor()
    try:
        cur.execute(
            f"SELECT amount FROM exchange_service.order_books where stock_id = {1} and operation = 'buy' and price = {price} order by price LIMIT 1")
        amount = cur.fetchall()[0][0]
        print("amount: ", amount)
        if amount == 1:
            cur.execute(
                f"DELETE FROM exchange_service.order_books where stock_id = {1} and price = {price} and amount = 1 and operation = '{operation}'")
        else:
            cur.execute(
                f"Update exchange_service.order_books SET amount = {amount - 1} where stock_id = 1 and price = {price} and operation = '{operation}'")
        cur.fetchall()
        con.commit()
    except Exception as e:
        pass
    finally:
        cur.close()
