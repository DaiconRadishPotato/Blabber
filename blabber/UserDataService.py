'''
Database service functions
'''
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class GuildDataService:
	#create connection in order to get prefix information from server table
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
		
	def set_guild_prefix(self, guild_id, prefix):
	
		insert_guild_query = '''INSERT INTO guilds(guild_id, prefix) 
		VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = %s'''
		
		guild_data = (guild_id, prefix, prefix)
		
		if self._cnx.is_connected() :
			cursor = self._cnx.cursor(buffered = True)
			
			try:
				cursor.execute(insert_guild_query, guild_data)	
				self._cnx.commit()
				return cursor.rowcount # returns 1 if added, 2 if updated
				print(count)
			except mysql.connector.Error as err: #used to catch duplicate keyerror
				print(err)
			finally:
				cursor.close()
		else:
			print('no connection found') # for debugging
			
	def get_guild_prefix(self, ch_id):
		'''get prefix through guild id'''
		
		query = '''SELECT prefix 
		FROM guilds 
		WHERE guild_id = %s 
		LIMIT 1'''
		
		data = (ch_id,)
		
		if self._cnx.is_connected():
			cursor = self._cnx.cursor(buffered=True)
			cursor.execute(query, data)
			record = cursor.fetchone()
			print(record)
			return record #returns dict
			cursor.close()	
		else:
			print('No connection found')
			
class UserDataService:
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
		
	def is_valid_voice_alias(self, voice_alias):
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
		
		user_data = (user_id, channel_id)
		
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
	
		insert_user_query = '''INSERT IGNORE INTO users (user_id, user_name) 
		VALUES (%s, %s)'''
		
		user_data = (user_id, username)
		
		if self._cnx.is_connected() :
			cursor = self._cnx.cursor(buffered = True)
			
			try:
				cursor.execute(insert_user_query, user_data)	
				self._cnx.commit()
				return cursor.rowcount # returns 1 if added
				print(count)
			except mysql.connector.Error as err: #used to catch duplicate keyerror
				print(err)
			finally:
				cursor.close()
		else:
			print('no connection found') # for debugging
	def set_voice_profile(self, user_id, channel_id, voice_alias):
		'''adds new user if user profile not in database, updates user profile if it is'''
		
		insert_voice_query = '''INSERT INTO voice_profiles 
		(user_id, channel_id, voice_alias) 
		VALUES ((SELECT user_id FROM users WHERE user_id = %s LIMIT 1), %s, %s) 
		ON DUPLICATE KEY UPDATE voice_alias = %s'''
		
		voice_data = (user_id, channel_id, voice_alias, voice_alias)
		
		if self._cnx.is_connected() :
			cursor = self._cnx.cursor(buffered = True)
			
			try:
				cursor.execute(insert_voice_query, voice_data)	
				self._cnx.commit()
				return cursor.rowcount # returns 1 if added, 2 if updated
				print(count)
			except mysql.connector.Error as err: #used to catch duplicate keyerror
				print(err)
			finally:
				cursor.close()
		else:
			print('no connection found') # for debugging
			
	def get_voice_profile(self, user_id, channel_id):
		''' Returns a string representing a voice '''
		
		query = '''SELECT * FROM available_voices AS av
		WHERE av.voice_alias IN 
		(SELECT voice_alias FROM voice_profiles 
		WHERE user_id = %s AND channel_id = %s)'''
	
		data=(user_id, channel_id)
		if self._cnx.is_connected():
			cursor = self._cnx.cursor(buffered=True)
			cursor.execute(query, data)
			record = cursor.fetchone()
			print(record) # for debugging 
			return record
			cursor.close()	
		else:
			print('no connection found') # for debugging		
