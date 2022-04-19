import pytest
from app import create_app, db
from app.models import Currency, Product, Event, ServiceFee


@pytest.fixture(scope = 'module')
def test_client():
    """ Fixture to create a test client"""
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test_db.db",
        "SECRET_KEY": '42:nice',
    })

    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client 


@pytest.fixture(scope = 'module')
def init_db(test_client):
    """Initialize the database"""
    db.create_all()

    # Create currency
    db.session.add(Currency(1, iso='USD'))

    # Create service fee
    db.session.add(ServiceFee(1, 1, amount=1.00))
    db.session.add(ServiceFee(2, 1, 1.50))
    db.session.add(ServiceFee(3, 1, 2.00))
    db.session.add(ServiceFee(4, 1, 2.50))

    # Create event
    db.session.add(Event(1, "Tomorrowland", 2))
    db.session.add(Event(2, "Back To The Future", 4))
    db.session.add(Event(3, "CarFest", 1))

    # Create product
    db.session.add(Product(1, 1, "T-shirt", 3))
    db.session.add(Product(2, 1, "VIP lounge", 4))
    db.session.add(Product(3, 2, "VIP lounge", 1))
    db.session.add(Product(4, 3, "VIP lounge", 4))
    db.session.add(Product(5, 1, "Ticket", 2))
    db.session.add(Product(6, 3, "Ticket", None))
    db.session.add(Product(7, 2, "Ticket", None))
    db.session.add(Product(8, 3, "Keychain", 1))

    db.session.commit()

    yield

    db.drop_all()
