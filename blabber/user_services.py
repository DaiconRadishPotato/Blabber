# user_service.py
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


class UserDataService:
    """
    Object that handles the connection, disconnection, and data updates
    pertaining to user data.
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
        
    def set_voice(self, user_id, channel_id, alias):
        """
        Creates and updates a voice profile for a user in a channel. A user can
        have a distinct voice profile on a given channel.
        
        parameters: 
            user_id [int]: id of the current user
            channel_id [int]: id of the current channel
            alias [str]: new voice 
        returns:
            int: 1 if voice was successfully added 2 if voice was updated.
            None: on connection failure
        """
        query = ("INSERT INTO voice_profiles " 
            "(user_id, channel_id, voice_alias) "
            "VALUES (%s, %s, %s) " 
            "ON DUPLICATE KEY UPDATE voice_alias = %s")
        data = (int(user_id), int(channel_id), str(alias), str(alias))
        
        if self._cnx.is_connected():
            cursor = self._cnx.cursor(buffered = True)
            
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
            
    def remove_voice(self, user_id, channel_id):
        """
        Removes specified row from the voice_profile table.
        
        parameters: 
            user_id [int]: id of the current user
            channel_id [int]: id of the current channel
        returns:
            int: 1 if voice was successfully removed.
            None: on connection failure
        """
        query = ("DELETE FROM voice_profiles "
            "WHERE user_id = %s AND channel_id = %s")
        data = (int(user_id), int(channel_id))
        
        if self._cnx.is_connected():
            cursor = self._cnx.cursor(buffered=True)
            
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
            
    def get_voice(self, user_id, channel_id):
        """
        Retrieves user's voice profile for a specified channel.
        
        parameters:
            user_id [int]: id of the current user 
            channel_id [int]: id of the current guild
        returns: 
            tuple: voice profile retrieved from the database
            None: if no record found in the table
        """ 
        query = ("SELECT * FROM available_voices "
            "WHERE voice_alias IN (SELECT voice_alias FROM voice_profiles "
            "WHERE user_id = %s AND channel_id = %s)")
        data = (int(user_id), int(channel_id))
        
        if self._cnx.is_connected():
            cursor = self._cnx.cursor(buffered=True)
            
            try:
                cursor.execute(query, data)
                record = cursor.fetchone() 
                return record
                
            except mysql.connector.Error as err:
                print(err)
                
            finally:
                cursor.close()
                
        else:
            print('no connection found') # for debugging
            