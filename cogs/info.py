# info.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 5/28/2020
# Python Version: 3.8.1
# License: MIT License

import json

from discord import Embed, Colour
from discord.ext import commands

from blabber.checks import *
from blabber.errors import *


class Info(commands.Cog):
    """
    Collection of commands for displaying information about Blabber Bot for the
    particular guild.

    parameters:
        bot [discord.Bot]: discord Bot object
    """

    def __init__(self, bot):
        self.MAX_EMBED_FIELDS = 25
        self.prefixes = bot.prefixes

        with open(r'./blabber/data.json', 'r') as data:
            self._voices_map = json.load(data)['voice_info']

    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        Prints out description of all available commands for Blabber to the
        text channel where the bot was invoked.

        paramters:
            ctx [Context]: context object representing command invocation
        """
        embed = Embed(title="Help Directory",
                      description="",
                      colour=Colour.blue())
        prefix = self.prefixes[ctx.guild]

        # Generate help for voice.py functions
        embed.add_field(name=f"`{prefix}connect` or `{prefix}c`",
                        value="Connect/Move Blabber into the voice channel you"
                        "are in",
                        inline=False)
        embed.add_field(name=f"`{prefix}disconnect` or `{prefix}dc`",
                        value="Disconnect Blabber from its voice channel",
                        inline=False)
        embed.add_field(name=f"`{prefix}say [message]` or `{prefix}s "
                        "[message]`",
                        value="Tell Blabber to say something. If Blabber is "
                        "not in the same voice channel, then it will join.",
                        inline=False)

        # Generate help for info.py functions
        embed.add_field(name=f"`{prefix}help` or `{prefix}h`",
                        value=f"Displays this message.",
                        inline=False)
        embed.add_field(name=f"`{prefix}list` or `{prefix}l`",
                        value="Displays the Voice Directory and voices.",
                        inline=False)

        # Generate help for profiles.py functions
        embed.add_field(name=f"`{prefix}voice [alias]` or `{prefix}v [alias]`",
                        value="Set a specific voice for your say commands "
                        "unique to the guild",
                        inline=False)

        # Generate help for settings.py functions
        embed.add_field(name=f"`{prefix}settings`",
                        value="Displays settings menu, which allows the "
                        "certain users to change Blabber Bot settings such as "
                        "the prefix",
                        inline=False)
        embed.add_field(name=f"`{prefix}settings prefix` or `{prefix}settings "
                        "p`", 
                        value="Displays current guild prefix.",
                        inline=False)

        # Generate help for roles.py functions
        embed.add_field(name=f"`{prefix}give_blabby [user]` or "
                        f"`{prefix}gb [user]`", 
                        value="Gives blabby role to user so they have priorty"
                        "when using blabber.",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.group(name='list', aliases=['l', 'ls'])
    async def list_available_voices(self, ctx):
        """
        Displays list voice options for the user to display a filter
        version based on either gender or language.

        parameters:
            ctx [Context]: context object representing command invocation
        """
        # Check if subcommand invoked
        if ctx.invoked_subcommand is None:
            prefix = self.prefixes[ctx.guild]
            embed = Embed(title="Voice Directory", description="Use the "
                          f"command `{prefix}list [option]`"
                          "to show filter options.",
                          colour=Colour.blue())

            # Generate information about possible subcommands
            embed.add_field(name="Gender",
                            value=f"`{prefix}list gender`",
                            inline=False)
            embed.add_field(name="Language",
                            value=f"`{prefix}list language`",
                            inline=False)

            await ctx.send(embed=embed)

    @list_available_voices.command(name='gender', aliases=['g'])
    async def voice_gender_filter(self, ctx, gender: str=''):
        """
        Subcommand of list that displays all available voices that have the
        specified gender.

        parameters:
            ctx [Context]: context object representing command invocation
            gender [str]: string object representing a gender option
        """
        gender = gender.upper()

        # Check if a gender was provided
        if not gender:
            prefix = self.prefixes[ctx.guild]

            # Create a string of all the available genders
            genders = ", ".join(gender for gender in supported_genders)

            embed = Embed(title="List of Voices - Gender Filter", 
                          colour=Colour.gold())

            embed.add_field(name=f"Available Genders Options:",
                            value=f"`{genders}`",
                            inline=False)

            embed.add_field(name="To list voices filtered by a gender:",
                            value=f"`{prefix}list gender [gender_option]`",
                            inline=False)
        else:
            # Ensure that gender is supported
            await gender_is_valid(gender)

            # Generate a list of available voices of a particular gender
            records = [
                (voice, info['language'], info['gender'])
                for voice, info in self._voices_map.items()
                if info['gender'] == gender
            ]

            # Create embed of all the available voices with the particular gender
            page_num = 1
            embed = Embed(title="Voice Directory - List of Voices"
                        " - Gender Filter - Page " + str(page_num),
                        colour=Colour.blue())

            for record_num in range(len(records)):
                alias = records[record_num]

                # Check if the number of fields in the embed had exceed 25
                if (record_num % (self.MAX_EMBED_FIELDS + 1) ==
                        self.MAX_EMBED_FIELDS):
                    await ctx.send(embed=embed)
                    page_num += 1
                    embed = Embed(title="Voice Directory - List of Voices"
                                " - Gender Filter - Page " + str(page_num),
                                colour=Colour.blue())

                embed.add_field(name=f"{alias[0]}",
                                value=f"language: {alias[1]}\ngender: {alias[2]}",
                                inline=True)

        await ctx.send(embed=embed)

    @list_available_voices.command(name='language', aliases=['lang'])
    async def voice_language_filter(self, ctx, language: str=''):
        """
        Subcommand of list that displays all available voices that have the
        specified language.

        parameters:
            ctx [Context]: context object representing command invocation
            language [str]: string object representing a language option
        """
        language = language.lower()

        # Check if language was provided
        if not language:
            prefix = self.prefixes[ctx.guild]

            # Create a string of all available languages
            languages = ", ".join(
                sorted(lang for lang in supported_languages.keys())
                )
            embed = Embed(title="List of Voices - Language Filter",
                          colour=Colour.gold())

            embed.add_field(name='Available Languages Options:',
                            value=f"`{languages}`",
                            inline=False)

            embed.add_field(name="To list voices filtered by a language:",
                            value=f"`{prefix}list lang [language_option]`",
                            inline=False)
        else:
            # Ensure that language is supported
            await language_is_valid(language)

            # Generate a list of available voices of a particular language
            records = [
                (voice, info['language'], info['gender'])
                for voice, info in self._voices_map.items()
                if info['language'] == language
            ]

            # Create embed of all the available voices with the particular language
            page_num = 1
            embed = Embed(title="Voice Directory - List of Voices - "
                        "Language Filter - Page " + str(page_num),
                        colour=Colour.blue())

            for record_num in range(len(records)):
                alias = records[record_num]

                # Check if the number of fields in the embed had exceed 25
                if (record_num % (self.MAX_EMBED_FIELDS + 1) ==
                        self.MAX_EMBED_FIELDS):
                    await ctx.send(embed=embed)
                    page_num += 1
                    embed = Embed(title="Voice Directory - List of Voices"
                                " - Language Filter - Page " + str(page_num),
                                colour=Colour.blue())

                embed.add_field(name=f"{alias[0]}",
                                value=f"language: {alias[1]}\ngender: {alias[2]}",
                                inline=True)
        await ctx.send(embed=embed)

    @voice_gender_filter.error
    async def voice_gender_filter_error(self, ctx, error):
        """
        Local error handler for subcommand list gender.
        If no gender argument, display how to invoke command.
        If key error, display the invalid argument and valid arguments.

        parameters:
            ctx [Context]: context object produced by a command invocation
            error [Exception]: error object thrown by command function
        """
        if isinstance(error, GenderNotSupported):
            prefix = self.prefixes[ctx.guild]

            embed = Embed(title="List of Voices - Gender Filter", 
                          colour=Colour.red())
            embed.add_field(name="Input Gender:",
                            value=f"{error}")
            embed.add_field(name=f"To List Gender Filter Options:",
                            value=f"`{prefix}list gender`")

        await ctx.send(embed=embed)

    @voice_language_filter.error
    async def voice_language_filter_error(self, ctx, error):
        """
        Local error handler for subcommand list language.
        If no language argument, display how to invoke command.
        If key error, display the invalid argument and valid languages.

        parameters:
            ctx [Context]: context object produced by a command invocation
            error [Exception]: error object thrown by command function
        """
        if isinstance(error, LanguageNotSupported):
            prefix = self.prefixes[ctx.guild]

            embed = Embed(title="List of Voices - Language Filter",
                          colour=Colour.red())
            embed.add_field(name='Input Language:',
                            value=f"{error}",
                            inline=False)
            embed.add_field(name="To list language filter options:",
                            value=f"`{prefix}list lang`",
                            inline=False)

        await ctx.send(embed=embed)



def setup(bot):
    """
    Removes templated help function and adds Help Cog to bot.

    parameter:
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Info(bot))
