import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '1234')
    MYSQL_DB = os.getenv('MYSQL_DB', 'supplytrack')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # App Configuration
    DEBUG = os.getenv('DEBUG', True)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supplytrack-secret-key-2024')