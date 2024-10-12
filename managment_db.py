# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# connect = psycopg2.connect(user='postgres', password='1111')
# connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# cursor = connect.cursor()

import sqlite3


connect = sqlite3.connect('warehouse.db')
cursor = connect.cursor()


cursor.execute('drop table if exists product')
cursor.execute('drop table if exists orders')
cursor.execute('drop table if exists order_item')

cursor.execute('''
    create table if not exists product (
        id integer primary key autoincrement,
        name text,
        description text,
        price int, 
        count int
    )
''')

cursor.execute('''
    create table if not exists orders (
        id integer primary key autoincrement,
        date date,
        status text
    )
''')

cursor.execute('''
    create table if not exists order_item (
        id integer primary key autoincrement,
        order_id integer,
        product_id integer,
        count integer,
        foreign key (order_id) references orders(id),
        foreign key (product_id) references product(id)
    )
''')

connect.commit()
connect.close()