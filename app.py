from flask import Flask
from flask_cors import CORS
from Controllers.userController import user_bp
from Controllers.linkController import link_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(link_bp)
