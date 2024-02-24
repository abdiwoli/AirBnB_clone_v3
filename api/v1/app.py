# api/v1/app.py
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    #host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    #port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host='0.0.0.0', port=5000, threaded=True)
