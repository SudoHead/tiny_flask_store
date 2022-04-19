from select import select
from . import db
from flask import Blueprint, render_template, session, request, \
    redirect, url_for, flash
from collections import defaultdict, namedtuple
from werkzeug.exceptions import BadRequestKeyError
from app.models import Currency, Product, Event, ServiceFee

store_bp = Blueprint('store_bp', __name__)

# used to pass the calculated data to the template
Total = namedtuple('Total', ['total_cost', 'total_service_fee'])


def add_cart(cart, product_id: str, quantity: int):
    """Adds a product to the cart. 
    If the product is already in the cart, adds the additional quantity.
    The cart is stored as a dict with the product_id as the key.
    Example:
    {
        int: {'event': str, 'quantity': int, 'cost': str, 'service_fee': numeric}
    }

    Args:
        product_id (str): id of the product to add as str.
        quantity (int): quantity of the product to add.

    Returns:
        dict: return the updated cart.
    """
    if not cart:
        cart = {}
    if quantity < 1:
        flash(f'Quantity must be greater than 0.', category='error')
        return cart

    try:
        product = db.session.query(Product).filter_by(id = product_id).first()
        if not product: raise AttributeError()
    except AttributeError:
        flash(f'Product id={product_id} not found.', category='error')
        return cart

    # use event service fee if product has no service fee
    if not product.service_fee:
        service_fee = float(product.event.service_fee.amount)
    else:
        service_fee = float(product.service_fee.amount)

    # NOTE: this assumes ALL product cost 10
    entry = {'event': product.event.name,
            'name': product.name, 
            'quantity': quantity,
            'cost': 10 * quantity,
            'price': 10, 
            'service_fee': service_fee * quantity}

    # if product already in cart, update quantity
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
        cart[product_id]['cost'] += entry['cost']
        cart[product_id]['service_fee'] += entry['service_fee']
    else:
        cart[product_id] = entry
    return cart


def get_total(cart) -> Total:
    """Calculates the total cost and service fee of the cart.

    Returns:
        Total: named tuple with total cost and service fee.
    """
    if not cart:
        return Total(0, 0)
    cost = 0
    service_fee = 0
    try:
        for _, item in cart.items():
            cost += float(item['cost'])
            service_fee += float(item['service_fee'])
    except TypeError:
        flash(f"item[cost]={item['cost']} type = {type(item['cost'])}", category='error')
        return Total(0, 0)
    return Total(cost, service_fee)


def get_products(event_id: int) -> list:
    """Return a list of products for a given event.

    Args:
        event_id (int): id of the event to get products for.

    Returns:
        list[Product]: list of products for the given event.
    """
    if not event_id:
        return []
    try:
        products = db.session.query(Product).filter_by(event_id=event_id).all()
    except AttributeError:
        flash(f'Event id={event_id} not found.', category='error')
        return []
    return products


@store_bp.route('/store', methods=['GET', 'POST'])
def store():
    """Renders the store page.
    """
    events = db.session.query(Event).all()
    selected_event = None
    if request.method == 'POST':
        selected_event = request.form.get('event')
    elif events:
        selected_event = events[0].id
    products = get_products(selected_event)
    return render_template('store.jinja',
        events = events,
        selected_event = selected_event,
        products = products,
        cart = session.get('cart', {}),
        total = get_total(session.get('cart', {})),
        )


@store_bp.route('/add_product', methods=['POST'])
def add_product():
    try:
        product_id = request.form.get('product')
        quantity = int(request.form.get('quantity'))
        if quantity < 1 or quantity > 999:
            raise ValueError('Quantity must be between 1 and 999.')
    except ValueError:
        flash(f'Invalid product id or quantity', 
        category='error')
    else:
        session['cart'] = add_cart(session.get('cart', {}), product_id, quantity)
        # tells Flask to update the session cookie to the client
        session.modified = True
    return redirect(url_for('store_bp.store'))


@store_bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    """Clears the cart by removing the session variable.
    """
    session.pop('cart', default = None)
    return redirect(url_for('store_bp.store'))


@store_bp.errorhandler(BadRequestKeyError)
def handle_bad_requests(e):
    """On bad requests (400):
        - notify error with flash and redirect;
        - redirect to the main store page.
    """
    flash("Error while adding product... please try again.", category='error')
    return redirect(url_for('store_bp.store'))