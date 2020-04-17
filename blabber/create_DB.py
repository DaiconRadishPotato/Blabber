import os
from dotenv import load_dotenv
load_dotenv()
from google.cloud import texttospeech
from google.cloud.texttospeech import enums
import json
import mysql.connector
from user_services import UserDataService
from guild_services import GuildDataService

def create_blabber_db():
    """
    One time facilitator to create the database and add mock data
    """
    try:
        cnx = mysql.connector.connect(
            user = os.getenv("db_user"),
            password = os.getenv("db_pw"),
            host = os.getenv("db_host")
        )
        #delete database
        cursor = cnx.cursor()
        name=os.getenv('db_name')
        drop_sql="DROP DATABASE IF EXISTS "+name
        print("Preparing to drop all existing tables...")
        cursor.execute(drop_sql)
        print("...Done")
        
        #create database
        create_sql="CREATE DATABASE "+name
        use_sql = "USE "+name
        print("Creating database...")
        cursor.execute(create_sql)
        cursor.execute(use_sql)
        
        print("Creating tables...")
        
        #creating vocice_profiles table
        cursor.execute("CREATE TABLE voice_profiles (user_id BIGINT NOT NULL, channel_id BIGINT NOT NULL, voice_alias VARCHAR(20) DEFAULT 'voice_1', PRIMARY KEY (user_id, channel_id))")
        print("Created voice_profiles")
        
        #creating available_voices table
        cursor.execute("CREATE TABLE available_voices (voice_alias VARCHAR(35) NOT NULL, voice_name VARCHAR(35), gender ENUM('FEMALE', 'MALE', 'NEUTRAL'), language VARCHAR(5), lang_code VARCHAR(10), PRIMARY KEY(voice_alias))")
        print("Created available_voices")
        
        #creating guild table
        cursor.execute("CREATE TABLE guilds (guild_id BIGINT NOT NULL, prefix VARCHAR(5) NOT NULL, PRIMARY KEY (guild_id))")
        print("Created all tables.")
        print("Created guilds")
        print("...Done")
        
    except mysql.connector.Error as err:
        print(err)
        
    else:
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
    else:    
        cursor.close()
        cnx.close()
        
def populate_tables_test_data():
    
    with open('blabber/test/MOCK_DATA.json', 'r') as f:
        mock_data_dict = json.load(f)
        
        uds = UserDataService()
        gds = GuildDataService()
        
    for data in mock_data_dict:
        uds.set_voice(data['user_id'], data['channel_id'], data['voice_alias'])
        gds.set_guild_prefix(data['guild_id'], data['prefix'])
        print(data['guild_id'])
        
if __name__=='__main__':
    create_blabber_db()
    populate_available_voice_table()
    populate_tables_test_data()