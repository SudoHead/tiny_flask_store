"""
Tests for models.py
"""

from app.models import Currency, Product, Event, ServiceFee


def test_currency_model():
    """
    GIVEN a Currency model
    WHEN a Currency object is created
    THEN check id, iso
    """
    currency = Currency(id = 1, iso = 'USD')
    assert currency.id == 1
    assert currency.iso == 'USD'


def test_event_model():
    """
    GIVEN an Event model
    WHEN an Event object is created
    THEN check id, name
    """
    event = Event(id = 1, name = 'Event 1', service_fee_id = 1)
    assert event.id == 1
    assert event.name == 'Event 1'
    assert event.service_fee_id == 1

def test_product_model():
    """
    GIVEN a Product model
    WHEN a Product object is created
    THEN check id, event_id, name
    """
    product = Product(id = 1, event_id = 1, name = 'Product 1', service_fee_id=None)
    assert product.id == 1
    assert product.event_id == 1
    assert product.name == 'Product 1'
    assert product.service_fee_id == None


def test_service_fee_model():
    """
    GIVEN a ServiceFee model
    WHEN a ServiceFee object is created
    THEN check id, currency_id, amount
    """
    service_fee = ServiceFee(id = 1, currency_id = 1, amount = 1.00)
    assert service_fee.id == 1
    assert service_fee.currency_id == 1
    assert service_fee.amount == 1.00


def test_servicefee_currency_relationship():
    """
    GIVEN a ServiceFee model
    WHEN a ServiceFee object is created
    THEN check relationship with Currency
    """
    currency = Currency(id = 1, iso = 'USD')
    service_fee = ServiceFee(id = 1, currency_id = 1, amount = 1.00)
    service_fee.currency = currency
    assert currency == service_fee.currency


def test_product_event_relationship():
    """
    GIVEN an Product model
    WHEN an Product object is created
    THEN check relationship with Event
    """
    event = Event(id = 1, name = 'Event 1', service_fee_id = 1)
    product = Product(id = 1, event_id = 1, name = 'Product 1', service_fee_id = 1)
    product.event = event
    assert event == product.event


def test_product_servicefee_relationship():
    """
    GIVEN a Product model
    WHEN a Product object is created
    THEN check relationship with ServiceFee
    """
    product = Product(id = 1, event_id = 1, name = 'Product 1', service_fee_id = 1)
    service_fee = ServiceFee(id = 1, currency_id = 1, amount = 1.00)
    product.service_fee = service_fee
    assert product.service_fee == service_fee
