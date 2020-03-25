import os
from dotenv import load_dotenv
load_dotenv()
from google.cloud import texttospeech
from google.cloud.texttospeech import enums
import json
import mysql.connector
from UserDataService import GuildDataService, UserDataService

def create_blabber_db():
	try:
		cnx = mysql.connector.connect(
			user = os.getenv("db_user"),
			password = os.getenv("db_pw"),
			host = os.getenv("db_host"),
			database = os.getenv("db_name")
		)
		
		cursor = cnx.cursor()
		print("Preparing to drop all existing tables...")
		cursor.execute("DROP TABLE IF EXISTS users")
		print("Dropped users")
		cursor.execute("DROP TABLE IF EXISTS voice_profiles")
		print("Dropped voice_profiles")
		cursor.execute("DROP TABLE IF EXISTS available_voices")
		print("Dropped available_voices")
		cursor.execute("DROP TABLE IF EXISTS channel_profile")
		print("Dropped channel_profile")
		print("...Done")
		
		print("Creating tables...")
		cursor.execute("CREATE TABLE users (user_id BIGINT NOT NULL, user_name VARCHAR(40) NOT NULL, Primary Key(user_id))")
		print("Created users")
		cursor.execute("CREATE TABLE voice_profiles (user_id BIGINT NOT NULL REFERENCES users(user_id), channel_id BIGINT NOT NULL, voice_alias VARCHAR(20) DEFAULT 'voice_1', PRIMARY KEY (user_id, channel_id))")
		print("Created voice_profiles")
		cursor.execute("CREATE TABLE available_voices (voice_alias VARCHAR(35) NOT NULL, voice_name VARCHAR(35), gender ENUM('FEMALE', 'MALE'), language VARCHAR(5), lang_code VARCHAR(10), Primary Key(voice_alias))")
		print("Created available_voices")
		cursor.execute("CREATE TABLE guilds (guild_id BIGINT NOT NULL, prefix VARCHAR(5) NOT NULL, Primary Key (guild_id))") #add default
		print("Created all tables.")
		print("Created guilds")
		print("...Done")
		
	except mysql.connector.Error as err:
		print(err)
		
	finally:	
		cursor.close()
		cnx.close()
		
def populate_available_voice_table():

	client = texttospeech.TextToSpeechClient()
	voices = client.list_voices()
	
	voice_count = 0
	
	add_voice = '''INSERT INTO available_voices 
	(voice_alias, voice_name, language, lang_code, gender) 
	VALUES(%(voice_alias)s, %(voice_name)s, %(language)s,  %(lang_code)s, %(gender)s)'''
	
	try:
		cnx = mysql.connector.connect(
			user = os.getenv('db_user'),
			password = os.getenv('db_pw'),
			host = os.getenv('db_host'),
			database = os.getenv('db_name')
		)
		
		cursor = cnx.cursor()

		for voice in voices.voices:
			
			if "Standard" in voice.name:
				#voice_alias voice_name language, lang_code gender
				alias = 'voice'
				voice_name = ''
				language = ''
				lang_code = ''
				gender = ''
				
				print('Name: {}'.format(voice.name))
				voice_name = voice.name # to add to db
				voice_count += 1
				
				for language_code in voice.language_codes:
					lang_code = language_code # to add to db
					print('Supported language_code:{}'.format(language_code))
					
					language =language_code.split('-',1)[0]
					print('Supported language:{}'.format(language))
					
				ssml_gender = enums.SsmlVoiceGender(voice.ssml_gender)
				
				print('SSML gender: {}'.format(ssml_gender.name))
				
				gender = ssml_gender.name #add to db
				
				data_voice = {
					'voice_alias':f'{alias}_{voice_count}',
					'voice_name':voice_name,
					'language': language,
					'lang_code':lang_code,
					'gender':gender,
				}

				cursor.execute(add_voice, data_voice)
				cnx.commit()
			else:
				continue		
	except mysql.connector.Error as err:
		print(err)
		print("ERROR CODE: ", err.errno)
		print("MESSAGE: ", err.msg)
	finally:	
		cursor.close()
		cnx.close()

def populate_tables_test_data():
	print('TODO: POPULATE user table with test data')
	
	with open('./test/MOCK_DATA.json', 'r') as f:
		mock_data_dict = json.load(f)
	
		uds = UserDataService()
		gds = GuildDataService()
		
	for data in mock_data_dict:
	#add data into table.
		uds.add_user(data['user_id'], data['user_name'])
		uds.set_voice_profile(data['user_id'], data['channel_id'], data['voice_alias'])
		gds.set_guild_prefix(data['guild_id'], data['prefix'])
		
if __name__=='__main__':
	create_blabber_db()
	populate_available_voice_table()
	populate_tables_test_data()