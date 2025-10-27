from flask import Flask, send_from_directory
from flask_cors import CORS
from Controllers.userController import user_bp
from Controllers.linkController import link_bp
import logging
import os

app = Flask(__name__)
CORS(app)

log_path = os.path.join("/tmp", "app.log")

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

app.register_blueprint(user_bp)
app.register_blueprint(link_bp)
