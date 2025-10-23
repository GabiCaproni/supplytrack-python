import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._create_connection()
        return cls._instance
    
    def _create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root', 
                password='1234',
                database='supplytrack',
                charset='utf8'
            )
            if self.connection.is_connected():
                print("✓ Conectado ao banco SupplyTrack")
        except Error as e:
            print(f"✗ Erro de conexão: {e}")
            self.connection = None

def execute_query(sql, params=None, fetch=False, fetch_all=False):
    """Executa queries no banco de dados"""
    db = DatabaseConnection()
    if not db.connection:
        return None
    
    try:
        cursor = db.connection.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        
        if fetch:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            db.connection.commit()
            result = cursor.lastrowid
        
        cursor.close()
        return result
        
    except Error as e:
        print(f"✗ Erro ao executar query: {e}")
        return None