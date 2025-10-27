from app import app  # se o app.py está na raiz
from vercel_python_wsgi import make_handler

handler = make_handler(app)
