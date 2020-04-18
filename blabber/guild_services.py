# guild_services.py
#
# Author: Fanny Avila (Fa-Avila),
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/10/2020
# Date last modified: 4/17/2020
# Python Version: 3.8.1
# License: "MIT"

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class GuildDataService:
    """
    Object that handles the connection, disconnection, and data updates
    pertaining to guild data.
    """
    def __init__(self):
        """Initializes connection to database"""
        self._cnx = mysql.connector.connect(
            user = os.getenv('db_user'),
            password = os.getenv('db_pw'),
            host = os.getenv('db_host'),
            database = os.getenv('db_name')
        )
        
    def __del__(self):
        """closes connection"""
        self._cnx.close()
        
    def set_guild_prefix(self, guild_id, prefix):
        """
        Creates and updates the guild prefix in the database.
        
        parameters: 
            guild_id [int]: id of the current guild
            prefix [str]: new prefix
        returns:
            int: 1 if voice was successfully added 2 if voice was updated.
            None: on connection failure
        """ 
        query = ("INSERT IGNORE INTO guilds (guild_id, prefix) " 
            "VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = %s")
        data = (int(guild_id), str(prefix), str(prefix))
        
        if self._cnx.is_connected():
            cursor = self._cnx.cursor(buffered=True)
            
            try:
                cursor.execute(query, data)
                self._cnx.commit()
                return cursor.rowcount # returns 1 if added, 2 if updated
                
            except mysql.connector.Error as err:
                print(err)
                
            finally:
                cursor.close()
                
        else:
            print('no connection found')
            
    def remove_guild_prefix(self, guild_id):
        """
        Removes specified row from the guilds table.
        
        parameters: 
            guild_id [int]: id of the current guild
        returns:
            int: 1 if voice was successfully removed.
            None: on connection failure
        """
        query = ("DELETE FROM guilds WHERE guild_id = %s")
        data = (int(guild_id),)
        
        if self._cnx.is_connected():
            cursor=self._cnx.cursor(buffered=True)
            
            try:
                cursor.execute(query, data)
                self._cnx.commit()
                return cursor.rowcount
                
            except mysql.connector.Error as err:
                print(err)
                
            finally:
                cursor.close()
                
        else:
            print('no connection found') # for debugging
            
    def get_guild_prefix(self, guild_id):
        """
        Retrieves guild prefix for the specified guild
        
        parameters: 
            guild_id [int]: id of the current guild
        returns: 
            tuple: prefix retrieved from the database
            None: If no record was found in the table
        """ 
        query = ("SELECT prefix FROM guilds WHERE guild_id = %s LIMIT 1")
        data = (int(guild_id),)
        
        if self._cnx.is_connected():
            cursor = self._cnx.cursor(buffered=True)
            cursor.execute(query, data)
            record = cursor.fetchone()
            print(record)
            return record #returns tuple
            cursor.close()
        else:
            print('No connection found')
            