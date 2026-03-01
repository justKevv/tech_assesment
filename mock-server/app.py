from flask import Blueprint, Flask

app = Flask(__name__)

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/health')
def status():
    return {"status": "ok"}

app.register_blueprint(customers_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5000)