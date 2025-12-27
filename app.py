from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import limiter
from Controllers.userController import user_bp
from Controllers.linkController import link_bp
import logging

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://mylinks-352x.onrender.com",
            "http://localhost:8080"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
SWAGGER_URL = "/docs"
API_URL = "/openapi.yaml"

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "MyLinks API"}
)

limiter.init_app(app)

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app.register_blueprint(user_bp)
app.register_blueprint(link_bp)
app.register_blueprint(swaggerui_bp)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Muitas requisições. Tente novamente mais tarde.",
        "message": str(e.description)
    }), 429

@app.route("/openapi.yaml")
def get_openapi_spec():
    return send_file('openapi.yaml')

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "mylinks-api"
    }), 200

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "MyLinks API",
        "version": "1.0.0"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)