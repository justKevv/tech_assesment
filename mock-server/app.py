from collections import OrderedDict
from flask import Blueprint, Flask, abort, jsonify, request
import json

try:
    with open('data/customers.json', 'r') as f:
        customers_json = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading customers: {e}")
    customers_json = []

    
app = Flask(__name__)

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/health')
def server_status():
    return jsonify({"status": "ok"})

@customers_bp.route('/customers')
def get_all_customers():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    paginated_customers = customers_json[(page-1)*limit:limit*page]
    return jsonify(OrderedDict([
        ("data", paginated_customers),
        ("total", len(customers_json)),
        ("page", page),
        ("limit", limit)
    ]))

@customers_bp.route('/customer/<int:user_id>')
def get_customer(user_id):
    customer = next((c for c in customers_json if c['id'] == user_id), None)
    if customer is None:
        abort(404)
    return jsonify({"data": customer})

app.register_blueprint(customers_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)