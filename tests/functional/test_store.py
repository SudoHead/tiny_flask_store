"""
Test store.py blueprint with GET and POST requests.
"""

from app import store, db
from app.models import Product, Event, ServiceFee


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is NOT valid
    """
    response = test_client.get('/')
    assert response.status_code == 404


def test_store_page(test_client, init_db):
    """
    GIVEN a Flask application
    WHEN the '/store' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/store')
    assert response.status_code == 200
    assert b'Store' in response.data
    assert b'Event' in response.data
    assert b'Product' in response.data
    assert b'Quantity' in response.data
    assert b'Cart' in response.data
    assert b'Clear' in response.data


def test_select_event(test_client, init_db):
    """
    GIVEN a Flask application
    WHEN an event is selected and posted to the'/store' page (POST)
    THEN check the response contains filtered products
    """
    response = test_client.post('/store', data = {'event': '3'})
    assert response.status_code == 200
    assert b'Keychain' in response.data
    assert b'Ticket' in response.data
    assert b'VIP lounge' in response.data

    """
    GIVEN a Flask application
    WHEN an event is selected and posted to the'/store' page (POST)
    THEN check the response contains filtered products
    """
    response = test_client.post('/store', data = {'event': '1'})
    assert response.status_code == 200
    assert b'T-shirt' in response.data
    assert b'Ticket' in response.data
    assert b'VIP lounge' in response.data


def test_add_product(test_client, init_db):
    """
    GIVEN a cart
    WHEN a product is added to the cart
    THEN check cart is updated
    """
    product = db.session.query(Product).filter_by(id=1).first()
    cart = {
        1:  {'event': product.event.name,
            'name': product.name, 
            'quantity': 1,
            'cost': 10,
            'price': 10, 
            'service_fee': float(product.service_fee.amount)}
        }
    cart = store.add_cart(cart, 1, 1)
    assert cart[1]['quantity'] == 2
    assert cart[1]['cost'] == 20
    assert cart[1]['price'] == 10
    assert cart[1]['service_fee'] == 4.0
    cart = store.add_cart(cart, 2, 100)
    assert len(cart) == 2

    """
    GIVEN a cart, invalid product
    WHEN a product is added to the cart
    THEN check cart is updated
    """
    cart = store.add_cart({}, -1, -1)
    assert len(cart) == 0


def test_total(test_client, init_db):
    """
    GIVEN a cart
    WHEN a product is added to the cart
    THEN check total is correct
    """
    cart = store.add_cart({}, 1, 1)
    assert store.get_total(cart) == store.Total(10, 2.0)

    cart = store.add_cart(cart, 1, 9)
    assert store.get_total(cart) == store.Total(100, 20.0)

    cart = store.add_cart(cart, 2, 100)
    assert store.get_total(cart) == store.Total(1100, 270.0)


def test_clear_cart(test_client, init_db):
    """
    GIVEN a Flask application
    WHEN the '/clear_cart' page is requested (POST)
    THEN check cart is cleared
    """
    response = test_client.post('/clear_cart', follow_redirects=True)
    assert response.status_code == 200
    assert b'Store' in response.data