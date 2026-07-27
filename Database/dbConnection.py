from mysql.connector import pooling
from dotenv import load_dotenv 
from exceptions import DbConnectionError
import os

load_dotenv()

pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASS", ""),
    database=os.getenv("DB_NAME", "monastery_db"),
    pool_reset_session=True,
    connection_timeout = 10
)

class DbConnection:
    @staticmethod
    def get_connection():
        try:
            return pool.get_connection()
        except Exception as e:
            raise DbConnectionError(f"Database connection failed: {e}")