# info.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 5/29/2020
# Python Version: 3.8.1
# License: MIT License

from discord import Embed, Colour
from discord.ext import commands

from blabber import supported_languages, supported_voices
from blabber.checks import *
from blabber.errors import *


class Info(commands.Cog):
    """
    Collection of commands for displaying information about Blabber Bot for the
    particular guild.

    parameters:
        bot [Bot]: client object representing a Discord bot
    """
    def __init__(self, bot):
        self.MAX_EMBED_FIELDS = 25
        self.prefixes = bot.prefixes

    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        Prints out description of all available commands for Blabber to the
        text channel where the bot was invoked.

        paramters:
            ctx [Context]: context object representing command invocation
        """
        embed = Embed(title=":blue_book: Help Directory",
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
    async def list(self, ctx):
        """
        Displays list voice options for the user to display a filter
        version based on either gender or language.

        parameters:
            ctx [Context]: context object representing command invocation
        """
        # Check if subcommand invoked
        if not ctx.invoked_subcommand:
            prefix = self.prefixes[ctx.guild]
            embed = Embed(title=":book: Voice Directory",
                          description=f":information_source: **Use** `{prefix}list [Option]` **to see more filter options**",
                          colour=Colour.blue())

            # Generate information about possible subcommands
            embed.add_field(name="**Gender:**",
                            value=f"`{prefix}list gender`")
            embed.add_field(name="**Language:**",
                            value=f"`{prefix}list language`")

            await ctx.send(embed=embed)

    @list.command(name='gender', aliases=['g'])
    async def list_gender(self, ctx, gender: str=''):
        """
        Subcommand of list that displays all available voices that have the
        specified gender.

        parameters:
            ctx [Context]: context object representing command invocation
            gender  [str] (default=''): string object representing gender option
        """
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

        # Ensure that gender is supported
        elif await gender_is_valid(gender):
            gender = gender.upper()

            # Generate a list of available voices of a particular gender
            records = [
                (voice, info['language'], gender)
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

    @list.command(name='language', aliases=['lang'])
    async def list_language(self, ctx, language: str=''):
        """
        Subcommand of list that displays all available voices that have the
        specified language.

        parameters:
            ctx  [Context]: context object representing command invocation
            language [str] (default=''): string object representing
                                         language option
        """
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

        # Ensure that language is supported
        elif await language_is_valid(language):
            language = language.lower()

            lang_codes = supported_languages[language]
            # Generate a list of available voices of a particular language
            records = [
                (voice, language, info['gender'])
                for voice, info in supported_voices.items()
                if any(info['lang_code'] == lc for lc in lang_codes)
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

    @list_gender.error
    async def list_gender_error(self, ctx, error):
        """
        Local error handler for subcommand list gender.
        If no gender argument, display how to invoke command.
        If key error, display the invalid argument and valid arguments.

        parameters:
            ctx     [Context]: context object produced by a command invocation
            error [Exception]: error object thrown by command function
        """
        if isinstance(error, GenderNotSupported):
            prefix = self.prefixes[ctx.guild]

            embed = Embed(title="List of Voices - Gender Filter", 
                          colour=Colour.red())
            embed.add_field(name="Input Gender:",
                            value=f"{error}",
                            inline=False)
            embed.add_field(name=f"To List Gender Filter Options:",
                            value=f"`{prefix}list gender`",
                            inline=False)

        await ctx.send(embed=embed)

    @list_language.error
    async def list_language_error(self, ctx, error):
        """
        Local error handler for subcommand list language.
        If no language argument, display how to invoke command.
        If key error, display the invalid argument and valid languages.

        parameters:
            ctx     [Context]: context object produced by a command invocation
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
