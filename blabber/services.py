# services.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 4/22/2020
# Python Version: 3.8.1
# License: MIT License
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class ConnectionManager:
    """
    Manages connection to the database.
    """
    def __init__(self):
        """Initializes connection."""
        self._cnx = None
        
    def __enter__(self):
        """
        Starts connection to database.
        
        returns:
            self._cnx [MySQLConnection]: connection to database
        """
        self._cnx = mysql.connector.connect(
            user = os.getenv('db_user'),
            password = os.getenv('db_pw'),
            host = os.getenv('db_host'),
            database = os.getenv('db_name')
        )
        return self._cnx
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Closes connection to the database.
        """
        self._cnx.close()
        self._cnx=None
        
class DataServices():
    def __init__(self):
        pass
    def read(self, query, data):
        """
        Reads single record from the database using the query and data arguments.
        
        parameters:
            query [str]: SQL query string
            data [tuple]: Tuple of data that is used by the query
        returns:
            record [tuple]: single record from the database
        """
        with ConnectionManager() as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            record = cursor.fetchone()
            print(record)
            return record #returns tuple
        
    def write(self, query, data):
        """
        Writes data into the database using the query and data arguments.
        
        parameters:
            query [str]: SQL query string
            data [tuple]: Tuple of data that is used by the query
        returns:
            rowcount [int]: number of rows affected by writing in the database
        """
        with ConnectionManager() as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount
            
class FilterServices():
    def __init__(self):
        pass
    def read_all(self, query, data):
        """
        Reads multiple records from the database using the query and data 
        arguments.
        
        parameters:
            query [str]: SQL query string
            data [tuple]: Tuple of data that is used by the query
        returns:
            record [list[tuple]]: multiple records from the database
        """
        with ConnectionManager() as cnx:
            cursor = cnx.cursor()
            cursor.execute(query, data)
            record = cursor.fetchall()
            print(record)
            return record #returns list of tuples