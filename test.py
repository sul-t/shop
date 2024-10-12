import requests

def products():
    products = [
        {
            "id": 1,
            "name": "Помидор", 
            "description": "Спелый",
            "price": 233,
            "count": 15
        },
        {
            "id": 2,
            "name": "Дыня", 
            "description": "Желтая",
            "price": 1333,
            "count": 10
        },
        {
            "id": 3,
            "name": "Арбуз", 
            "description": "Гнилой",
            "price": 87,
            "count": 23
        }
    ]

    return products


def test_create_product():
    url = 'http://127.0.0.1:8000/products'

    for product in products():
        response = requests.post(url, json = product)
        
        assert response.status_code == 200


def test_all_products():
    url = 'http://127.0.0.1:8000/products' 
    response = requests.get(url)

    assert response.status_code == 200


def test_product_by_id():
    id = 1
    url = f'http://127.0.0.1:8000/products/{id}' 
    response = requests.get(url)

    assert response.status_code == 200


def test_update_product():
    id = 1  
    url = f'http://127.0.0.1:8000/products/{id}' 
    product = {
        "id": id,
        "name": "Кокос",
        "description": "Белый",
        "price": 555,
        "count": 23
    }

    response = requests.put(url, json=product)
    
    assert response.status_code == 200


def test_delete_product():
    id = 1  
    url = f'http://127.0.0.1:8000/products/{id}' 

    response = requests.delete(url)

    assert response.status_code == 200


def orders():
    orders = [
        {
            "name": "Дыня",
            "description": "Желтая",
            "count": 5
        },
        {
            "name": "Арбуз",
            "description": "Гнилой",
            "count": 5
        }
    ]

    return orders


def test_create_order():
    url = 'http://127.0.0.1:8000/orders' 
    for order in orders():
        response = requests.post(url, json=order)

        assert response.status_code == 200


def test_all_orders():
    url = 'http://127.0.0.1:8000/orders' 
    response = requests.get(url)

    assert response.status_code == 200


def test_order_by_id():
    id = 1
    url = f'http://127.0.0.1:8000/orders/{id}' 
    response = requests.get(url)

    assert response.status_code == 200

def test_update_status_order():
    id = 1
    url = f'http://127.0.0.1:8000/orders/{id}/status' 
    response = requests.patch(url, json={"status": "Отправлен"})

    assert response.status_code == 200

    id = 2
    url = f'http://127.0.0.1:8000/orders/{id}/status' 
    response = requests.patch(url, json={"status": "Доставлен"})

    assert response.status_code == 200
