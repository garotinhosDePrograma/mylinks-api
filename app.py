from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from Controllers.userController import user_bp
from Controllers.linkController import link_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(link_bp)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, "uploads"), filename)