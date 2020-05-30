# services.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 5/28/2020
# Python Version: 3.8.1
# License: MIT License

import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class ConnectionManager:
    """
    Manages connection to the database.

    parameters:
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

    def insert(self, user, channel, alias):
        """
        Creates and updates a voice profile for a user in a channel. A user 
        can have a distinct voice profile on a given channel.

        parameters:
            user       [User]: discord User Object
            channel [Channel]: discord Channel Object
            alias       [str]: string object representing a voice
        returns:
            int: integer representing successful insertion or update
        """
        query = ("INSERT INTO voice_profiles "
                 "(user, channel, voice_alias) "
                 "VALUES (%s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE voice_alias = %s")
        data = (int(hash(user)), int(hash(channel)), str(alias), str(alias))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount

    def select(self, user, channel):
        """
        Retrieves user's voice profile for a specified channel.

        parameters:
            user       [User]: discord User Object
            channel [Channel]: discord Channel object
        returns:
            tuple: voice profile retrieved from the database
        """
        query = ("SELECT voice_alias "
                 "FROM   voice_profiles "
                 "WHERE  user = %s AND channel = %s")
        data = (int(hash(user)), int(hash(channel)))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            return cursor.fetchone()

    def delete(self, user, channel):
        """
        Deletes specified row from the voice_profile table.

        parameters:
            user       [User]: discord User Object
            channel [Channel]: discord Channel object
        returns:
            int: integer representing a voice successfully removed
        """
        query = ("DELETE FROM voice_profiles "
                 "WHERE user = %s AND channel = %s")
        data = (int(hash(user)), int(hash(channel)))

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

    def insert(self, guild, prefix):
        """
        Creates and updates the guild prefix in the database.

        parameters:
            guild [Guild]: discord Guild object
            prefix  [str]: new prefix
        returns:
            int: integer representing successful insertion or update
        """
        query = ("INSERT INTO guilds (guild, prefix) "
                 "VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = %s")
        data = (int(hash(guild)), str(prefix), str(prefix))

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount

    def select(self, guild):
        """
        Retrieves user's voice profile for a specified channel.

        parameters:
            user       [User]: discord User Object
            channel [Channel]: discord Channel object
        returns:
            tuple: voice profile retrieved from the database
        """
        query = ("SELECT prefix FROM guilds WHERE guild = %s LIMIT 1")
        data = (int(hash(guild)),)

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            return cursor.fetchone()

    def delete(self, guild):
        """
        Removes specified row from the guilds table.

        parameters:
            guild [Guild]: discord Guild object
        returns:
            int: integer representing successful removal.
        """
        query = ("DELETE FROM guilds WHERE guild = %s")
        data = (int(hash(guild)),)

        with ConnectionManager(os.getenv('db_user'), os.getenv('db_pw')) as cnx:
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return cursor.rowcount
