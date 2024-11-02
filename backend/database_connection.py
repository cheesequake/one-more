import mysql.connector
import os
from mysql.connector import Error

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

def connect_to_rds ():
    """
    connect_to_rds function.

    :return: MySQLConnection object
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )

        if connection.is_connected():
            print("Connected to AWS RDS MySQL")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None