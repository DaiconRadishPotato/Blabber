# services.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 4/23/2020
# Python Version: 3.8.1
# License: MIT License

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class ConnectionManager:
    """
    Manages connection to the database.

    attributes:
        username [str]: username for connction to MySQLConnection
        password [str]: password for connction to MySQLConnection
    """

    def __init__(self, username, password):
        """Initializes connection."""
        self._cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=os.getenv('db_host'),
            database=os.getenv('db_name')
        )

    def __enter__(self):
        """
        Starts connection to database.

        returns:
            self._cnx [MySQLConnection]: connection to database
        """
        return self._cnx

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Closes connection to the database.
        """
        self._cnx.close()


class UserService:
    """
    Object that handles the connection, disconnection, and data updates
    pertaining to user data.
    """

    def __init__(self):
        pass

    def insert(self, user_id, channel_id, alias):
        """
        Creates and updates a voice profile for a user in a channel. A user 
        can have a distinct voice profile on a given channel.

        parameters:
            user_id [int]: id of the current user
            channel_id [int]: id of the current channel
            alias [str]: new voice
        returns:
            int: 1 if voice was successfully added 2 if voice was updated.
            None: On connection failure
        """
        query = ("INSERT INTO voice_profiles "
                 "(user_id, channel_id, voice_alias) "
                 "VALUES (%s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE voice_alias = %s")
        data = (int(user_id), int(channel_id), str(alias), str(alias))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount

    def select(self, user_id, channel_id):
        """
        Retrieves user's voice profile for a specified channel.

        parameters:
            user_id [int]: id of the current user
            channel_id [int]: id of the current guild
        returns:
            tuple: voice profile retrieved from the database
            None: if no record found in the table
        """
        query = (
            "SELECT * FROM available_voices "
            "WHERE voice_alias IN (SELECT voice_alias FROM voice_profiles "
            "WHERE user_id = %s AND channel_id = %s)")
        data = (int(user_id), int(channel_id))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    def delete(self, user_id, channel_id):
        """
        Deletes specified row from the voice_profile table.

        parameters:
            user_id [int]: id of the current user
            channel_id [int]: id of the current channel
        returns:
            int: 1 if voice was successfully removed.
            None: On connection failure
        """
        query = ("DELETE FROM voice_profiles "
                 "WHERE user_id = %s AND channel_id = %s")
        data = (int(user_id), int(channel_id))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount


class GuildService:
    """
    Object that handles the connection, disconnection, and data updates
    pertaining to guild data.
    """

    def __init__(self):
        pass

    def insert(self, guild_id, prefix):
        """
        Creates and updates the guild prefix in the database.

        parameters:
            guild_id [int]: id of the current guild
            prefix [str]: new prefix
        returns:
            int: 1 if voice was successfully added 2 if voice was updated.
            None: On connection failure
        """
        query = ("INSERT INTO guilds (guild_id, prefix) "
                 "VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = %s")
        data = (int(guild_id), str(prefix), str(prefix))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount

    def select(self, guild_id):
        """
        Retrieves user's voice profile for a specified channel.

        parameters:
            user_id [int]: id of the current user
            channel_id [int]: id of the current guild
        returns:
            tuple: voice profile retrieved from the database
            None: if no record found in the table
        """
        query = ("SELECT prefix FROM guilds WHERE guild_id = %s LIMIT 1")
        data = (int(guild_id),)

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    def delete(self, guild_id):
        """
        Removes specified row from the guilds table.

        parameters:
            guild_id [int]: id of the current guild
        returns:
            int: 1 if voice was successfully removed.
            None: On connection failure
        """
        query = ("DELETE FROM guilds WHERE guild_id = %s")
        data = (int(guild_id),)

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount
