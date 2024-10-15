from db_connect import session
from db_managment import ProductBase, OrdersBase, OrderItemBase

from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

from sqlalchemy import select



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
    query_product_id = session.query(ProductBase.id).filter(ProductBase.name == product['name'] and ProductBase.description == product['description']).first()
    
    if query_product_id is not None:
        return False

    data_product = ProductBase(name=product['name'], description=product['description'], price=product['price'], count=product['count'])
    session.add(data_product)
    session.commit()

    return True

# получение всех товаров
def all_products():
    list_products = session.scalars(select(ProductBase)).all()

    return list(list_products)

# получение информации о товаре по id
def product_by_id(id: int):
    product_data = session.scalars(select(ProductBase).where(ProductBase.id == id)).first()

    return product_data

# обновление данных товара
def update_product(id: int, update_data: dict):
    product = session.scalars(select(ProductBase).where(ProductBase.id == id)).one()

    product.name = update_data['name']
    product.description = update_data['description']
    product.price = update_data['price']
    product.count = update_data['count']

    session.commit()

    return True

# удаление товара
def dellete_product(id: int):
    product = session.get(ProductBase, id)
    session.delete(product)

    session.commit()

    return True

# создание заказа
def create_order(order: dict):
    new_name = order['name']
    new_description = order['description']
    new_count = order['count']

    query_product = session.query(ProductBase).filter(ProductBase.name == new_name and ProductBase.description == new_description).first()

    if query_product is None:
        return False
    
    if new_count > query_product.count:
        raise {'message': 'Недостаточное количество товара'}
    
    data_order = OrdersBase(date = datetime.now().date(), status = 'В процессе')
    session.add(data_order)
    session.flush()

    data_order_item = OrderItemBase(order_id = data_order.id, product_id = query_product.id, count = new_count)
    session.add(data_order_item)

    update_product = session.get(ProductBase, query_product.id)
    update_product.count = update_product.count - new_count

    session.commit()

    return True

# получение всех заказов
def all_orders():
    list_order = session.scalars(select(OrdersBase)).all()

    return list(list_order)

# получение информации о заказе по id
def order_by_id(id: int):
    product_data = session.scalars(select(OrdersBase.id, OrderItemBase.product_id, OrderItemBase.count, OrdersBase.date, OrdersBase.status).join(OrdersBase, OrderItemBase.order_id == OrdersBase.id).where(OrdersBase.id == id)).first()

    return product_data

# обновление статуса заказа
def update_status(id: int, new_status: UpdateStatus):
    update_order = session.scalars(select(OrdersBase).where(OrdersBase.id == id)).one()
    update_order.status = new_status['status']

    session.commit()

    return True
