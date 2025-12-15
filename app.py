from flask import Flask, jsonify
from flask_cors import CORS
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
        "methods": ["GET", "POST" "PUT" "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

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

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Muitas requisições. Tente novamente mais tarde.",
        "message": str(e.description)
    }), 429


@app.route("/health")
def health_check():
    return jsonify({
        "status": "ok", "service": "mylinks-api"
    }), 200

@app.route("/")
def root():
    return jsonify({
        "message": "MyLinks API",
        "version": "1.0.0"
    }), 200
