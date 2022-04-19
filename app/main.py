from . import create_app
from flask import redirect, url_for

app = create_app()

@app.route('/')
def main_page():
    return redirect(url_for('store_bp.store'))

app.run(host="0.0.0.0", port=80)