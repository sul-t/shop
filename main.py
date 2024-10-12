from fastapi import FastAPI, HTTPException
from utils import all_products, product_by_id, create_product, update_product, dellete_product, update_status, all_orders, order_by_id, create_order
from utils import Product, Order, UpdateStatus

from pydantic import ValidationError



app = FastAPI()



# GET запросы
# получение всех товаров
@app.get('/products')
def get_all_products():
    return all_products()

# получение информации о товаре по id
@app.get('/products/{id}')
def get_product_by_id(id: int):
    return product_by_id(id)


# получение всех заказов
@app.get('/orders')
def get_all_orders():
    return all_orders()

# получение информации о заказе по id
@app.get('/orders/{id}')
def get_order_by_id(id: int):
    return order_by_id(id)



# POST запросы
# создание товара
@app.post('/products')
def create_product_handler(product: Product):
    product_dict = product.dict()
    check = create_product(product_dict)

    if check:
        return {"message": "Продукт успешно добавлен!"}
    else:
        raise HTTPException(status_code=400, detail='Ошибка при добавлении продукта')
    

# создание заказа
@app.post('/orders')
def create_order_handler(order: Order):
    order_dict = order.dict()
    check = create_order(order_dict)

    if check:
        return {"message": "Ордер успешно создан!"}
    else:
        raise HTTPException(status_code=400, detail='Ошибка при создании ордера')



# PUT запросы
# обновление данных товара
@app.put('/products/{id}')
def update_product_by_id(id: int, new_data: Product):
    check = update_product(id, new_data.dict())

    if check:
        return {'message': 'Данные о товаре успешно обновлены'}
    else:
        raise HTTPException(status_code=400, detail='Ошбика при обновлении данных о товаре')



# DELETE запрос
# удаление товара
@app.delete('/products/{id}')
def delete_product_by_id(id: int):
    check = dellete_product(id)

    if check:
        return {'message': 'Товар успешно удален'}
    else:
        raise HTTPException(status_code=400, detail='Ошбика при удалении товара')



# PATCH запрос
@app.patch('/orders/{id}/status')
def update_order_status(id: int, status: UpdateStatus):
    check = update_status(id, status.dict())

    if check:
        return {'message': 'Статус успешно изменен'}
    else:
        raise HTTPException(status_code=400, detail='Ошбика при изменении статуса')