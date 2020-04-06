# UserDataService.py
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
      
class UserDataService:
  """
  Object that handles the connection, disconnection, and data updates
  pertaining to user data.
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
    
  def is_valid_voice(self, voice_alias):
    '''checks if voice exists in available_voices table in db'''
    
    query = '''SELECT EXISTS
    (SELECT * FROM available_voices 
    WHERE voice_alias = %s)'''
      
    data=(voice_alias,)
    
    if self._cnx.is_connected():
        cursor = self._cnx.cursor()
        cursor.execute(query, data) 
        print('in is valid voice')
        
        if cursor.fetchone()[0] == 1: # if exists return 1
          print(1)
          return 1
        else:
          return 0  
        cursor.close()
    else:
      print('no connection found') # for debugging
      
  def is_existing_user(self, user_id, channel_id):
    '''checks if user profile exists'''
    
    check_user_query = '''SELECT EXISTS
    (SELECT * From voice_profiles 
    WHERE user_id = %s AND channel_id = %s)'''
    
    user_data = (int(user_id), int(channel_id))
    
    if self._cnx.is_connected() :
      cursor = self._cnx.cursor()
      cursor.execute(query, data)
      if cursor.fetchone()[0] == 1: # if exists return 1
        return 1
      else:
        return 0  
      cursor.close()
    else:
      print('no connection found')    
  def add_user(self, user_id, username):
    """
    Adds user defined guild prefix into guild table
    
    parameters: 
      user_id: [int] id of the current user
      username: [str] username of current user 
    returns:
      [int] 1 if user was successfully added
    """ 
    
    insert_user_query = '''INSERT IGNORE INTO users (user_id, user_name) 
    VALUES (%s, %s)'''
    
    user_data = (int(user_id), username)
    
    if self._cnx.is_connected() :
      cursor = self._cnx.cursor(buffered = True)
      
      try:
        cursor.execute(insert_user_query, user_data)  
        self._cnx.commit()
        return cursor.rowcount # returns 1 if added
        print(count)
      except mysql.connector.Error as err:
        print(err)
      finally:
        cursor.close()
    else:
      print('no connection found') # for debugging
  def set_voice(self, user_id, channel_id, voice_alias):
    """
    Creates and updates new users profile in database if user's 
    information is already in users table.
    
    parameters: 
      user_id: [int] id of the current user
      channel_id: [int] id of the current channel
      voice alias: [str] new voice 
    returns:
      [int] 1 if voice was successfully added 2 if vocie was updated
    """
    insert_voice_query = '''INSERT INTO voice_profiles 
    (user_id, channel_id, voice_alias) 
    VALUES 
    ((SELECT user_id FROM users WHERE user_id = %s LIMIT 1), %s, %s) 
    ON DUPLICATE KEY UPDATE voice_alias = %s'''
    
    voice_data = (int(user_id), int(channel_id), voice_alias, voice_alias)
    
    if self._cnx.is_connected() :
      cursor = self._cnx.cursor(buffered = True)
      
      try:
        cursor.execute(insert_voice_query, voice_data)  
        self._cnx.commit()
        return cursor.rowcount # returns 1 if added, 2 if updated
        print(count)
      except mysql.connector.Error as err:
        print(err)
      finally:
        cursor.close()
    else:
      print('no connection found') # for debugging
      
  def get_voice(self, user_id, channel_id):
    """
    returns vocie profile from database base on user_id and channel_id
    
    parameters:
      user_id: [int] id of the current user 
      channel_id: [int] id of the current guild
    returns: 
      voice: [str] voice profile retrieved from the database
    """ 
    
    query = '''SELECT * FROM available_voices AS av
    WHERE av.voice_alias IN 
    (SELECT voice_alias FROM voice_profiles 
    WHERE user_id = %s AND channel_id = %s)'''
  
    data=(int(user_id), int(channel_id))
    if self._cnx.is_connected():
      cursor = self._cnx.cursor(buffered=True)
      cursor.execute(query, data)
      record = cursor.fetchone()
      print(record) # for debugging 
      return record
      cursor.close()  
    else:
      print('no connection found') # for debugging

