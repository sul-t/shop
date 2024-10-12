import sqlite3

from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime



# Статус заказа
class Status(str, Enum):
    in_process = 'В процессе'
    sent = 'Отправлен'
    delivered = 'Доставлен'

# Модель продуктов
class Product(BaseModel):
    name: str = Field(..., description='Название товара')
    description: str = Field(..., max_length=500, description='Описание, не более 500 символов')
    price: int = Field(..., ge=0, description='Цена цена')
    count: int = Field(..., ge=0, description='Колличество на складе')

# Модель заказа
class Order(BaseModel):
    name: str = Field(..., description='Укажите название товара')
    description: str = Field(..., max_length=500, description='Описание товара')
    count: int = Field(..., description='Колличество товара')

class UpdateStatus(BaseModel):
    status: Status = Field(..., description='Выбирите статус заказа')



# создание товара
def create_product(product: dict):
    connect = sqlite3.connect('warehouse.db')
    cursor = connect.cursor()

    if (cursor.execute('select id from product where name = ? and description = ?', (product['name'], product['description']))).fetchone() is not None:
        connect.close()
        return False
    

    cursor.execute('insert into product(name, description, price, count) values(?, ?, ?, ?)', (product['name'], product['description'], product['price'], product['count']))
    
    connect.commit()
    connect.close()

    return True

# создание словаря из запроса
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# получение всех товаров
def all_products():
    connect = sqlite3.connect('warehouse.db')
    connect.row_factory = dict_factory

    list_products = connect.cursor().execute('select * from product').fetchall()

    connect.close()
    return list_products

# получение информации о товаре по id
def product_by_id(id: int):
    connect = sqlite3.connect('warehouse.db')
    connect.row_factory = dict_factory

    product_data = connect.cursor().execute('select * from product where id = ?', (id,)).fetchone()

    return product_data

# обновление данных товара
def update_product(id: int, update_data: dict):
    connect = sqlite3.connect('warehouse.db')
    cursor = connect.cursor()

    cursor.execute('update product set name = ?, description = ?, price = ?, count = ? where id = ?', (update_data['name'], update_data['description'], update_data['price'], update_data['count'], id))
    
    connect.commit()
    connect.close()

    return True

# удаление товара
def dellete_product(id: int):
    connect = sqlite3.connect('warehouse.db')
    cursor = connect.cursor()

    cursor.execute('delete from product where id = ?', (id,))

    connect.commit()
    connect.close()

    return True

# создание заказа
def create_order(order: dict):
    connect = sqlite3.connect('warehouse.db')
    cursor = connect.cursor()

    new_name = order['name']
    new_description = order['description']
    new_count = order['count']

    product_id, product_count = cursor.execute('select id, count from product where name = ? and description = ?', (new_name, new_description)).fetchone()

    if product_id is None:
        return False
    
    if new_count > product_count:
        raise {'message': 'Недостаточное количество товара'}
    
    order_id = cursor.execute('insert into orders(date, status) values(?, ?) returning id', (datetime.now().date(), 'В процессе')).fetchone()[0]

    cursor.execute('insert into order_item(order_id, product_id, count) values(?, ?, ?)', (order_id, product_id, new_count))
    cursor.execute('update product set count = count - ? where id = ?', (new_count, product_id))
    
    connect.commit()
    connect.close()

    return True

# получение всех заказов
def all_orders():
    connect = sqlite3.connect('warehouse.db')
    connect.row_factory = dict_factory

    list_order = connect.cursor().execute('select * from orders').fetchall()

    connect.close()
    return list_order

# получение информации о заказе по id
def order_by_id(id: int):
    connect = sqlite3.connect('warehouse.db')
    connect.row_factory = dict_factory

    product_data = connect.cursor().execute('''
                                                select o.id, oi.product_id, oi.count, o.date, o.status 
                                                from orders as o 
                                                join order_item as oi on oi.order_id = o.id 
                                                where o.id = ?
                                            ''', (id,)).fetchone()

    return product_data

# обновление статуса заказа
def update_status(id: int, new_status: UpdateStatus):
    connect = sqlite3.connect('warehouse.db')
    cursor = connect.cursor()

    cursor.execute('update orders set status = ? where id = ?', (new_status['status'], id))

    connect.commit()
    connect.close()

    return True
