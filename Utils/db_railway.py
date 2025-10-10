import mysql.connector
import os
from urllib.parse import urlparse
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

connection_url = os.getenv('CONN_URL')
parsed_url = urlparse(connection_url)

config = {
    'host': parsed_url.hostname,
    'port': parsed_url.port,
    'user': parsed_url.username,
    'password': parsed_url.password,
    'database': parsed_url.path.lstrip('/'),
    'ssl_disabled': False,
}

def get_db():
    return mysql.connector.connect(**config)
