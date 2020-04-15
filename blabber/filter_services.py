# filter_service.py
# Author: Fanny Avila (Fa-Avila),
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/10/2020
# Date last modified: 3/24/2020
# Python Version: 3.8.1
# License: "MIT"

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class FilterServices():
    """
    Object that handles filtering available voices from database.
    """
    def __init__(self):
        '''Initializes connection to database'''
        self._cnx = mysql.connector.connect(
            user = os.getenv('db_user'),
            password = os.getenv('db_pw'),
            host = os.getenv('db_host'),
            database = os.getenv('db_name')
        )
        
    def __del__(self):
        self._cnx.close()
        
    def filter_by_gender(self, gender):
        """
        Filters available voices by gender
        
        arguments:
            gender:[str] string that represents gender
        returns:
            records: a list of tuples
        """
        if self._cnx.is_connected():
            query = '''SELECT voice_alias, language, gender FROM available_voices WHERE gender=%s'''
            data=(gender,)
            cursor=self._cnx.cursor()
            cursor.execute(query, data)
            records = cursor.fetchall()
            cursor.close()
            return records
        else:
            print("No Connection Found")
            
    def filter_by_lang(self, lang):
        """
        Filters available voices by language
        
        arguments:
            language:[str] string that represents language
        returns:
            records: a list of tuples
        """
        if self._cnx.is_connected():
            query = '''SELECT voice_alias, language, gender FROM available_voices WHERE language=%s'''
            data=(lang,)
            cursor=self._cnx.cursor()
            cursor.execute(query, data)
            records = cursor.fetchall()
            cursor.close()
            return records
        else:
            print("No Connection Found")