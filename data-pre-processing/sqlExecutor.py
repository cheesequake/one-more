import mysql.connector
from mysql.connector import Error

def connect_to_rds():
    """
    connect_to_rds

    Connect to your database where you want to store all data

    :return: A MySQLConnectionAbstract object
    """
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            passwd='',
            database='',
            port=0
        )

        if connection.is_connected():
            print("Connected to AWS RDS MySQL using admin credentials")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to execute any SQL statement
def execute_sql(connection, sql_query):
    """
    execute_sql

    Execute the passed statement on the connected database

    :param connection: A MySQLConnectionAbstract object which is connected to your database
    :param sql_query: An SQL query as String, to execute
    :return: A list of objects (if any)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        print("Query executed successfully")
        if cursor.rowcount > 0:
            return cursor.fetchall()
    except Error as e:
        print(f"Error executing SQL: {e}")
        return None
    finally:
        cursor.close()
