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
    #Connection to database
    self._cnx = mysql.connector.connect(
      user = os.getenv('db_user'),
      password = os.getenv('db_pw'),
      host = os.getenv('db_host'),
      database = os.getenv('db_name')
    )
    
  def __del__(self):
    self._cnx.close()
    
  def set_guild_prefix(self, guild_id, prefix):
    """
    Adds user defined guild prefix into guild table
    
    parameters: 
      guild_id: [int] id of the current guild
      prefix: [str] new prefix string 
    returns:
      [int] 1 if prefix was successfully added 2 if prefix was updated
    """ 
    insert_guild_query = '''INSERT IGNORE INTO guilds (guild_id, prefix) 
    VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = %s'''
    
    guild_data = (guild_id, prefix, prefix)
    
    if self._cnx.is_connected() :
      cursor = self._cnx.cursor(buffered = True)
      
      try:
        cursor.execute(insert_guild_query, guild_data)  
        self._cnx.commit()
        return cursor.rowcount # returns 1 if added, 2 if updated
        print(count)
      except mysql.connector.Error as err:
        print(err)
      finally:
        cursor.close()
    else:
      print('no connection found') # for debugging
      
  def get_guild_prefix(self, guild_id):
    """
    returns guild prefix from database base on guild_id
    
    parameters: 
      guild_id: [int] id of the current guild
    returns: 
      prefix: [str] prefix retrieved from the database
    """ 
    query = '''SELECT prefix FROM guilds WHERE guild_id = %s LIMIT 1'''
    
    data = (guild_id,)
    
    if self._cnx.is_connected():
      cursor = self._cnx.cursor(buffered=True)
      cursor.execute(query, data)
      record = cursor.fetchone()
      print(record)
      return record #returns dict
      cursor.close()  
    else:
      print('No connection found')

