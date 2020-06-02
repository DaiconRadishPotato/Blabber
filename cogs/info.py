# info.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 6/2/2020
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
        self.MAX_EMBED_FIELDS = 24
        self.prefixes = bot.prefixes

    def _voice_filter(self, field, *values):
        """
        Generator used for extracting voices to display.

        parameters:
            field    [str]: field to filter voices by
            values [tuple]: acceptable values
        yields:
            tuple: voice information to display 
        """
        for alias, info in supported_voices.items():
            # Extract voice region code
            region_code = info['lang_code'][-2:].lower()

            # Ensure region flag exists
            if region_code == 'xa':
                region = "`?`"
            else:
                region = f":flag_{region_code}:"

            # Extract voice gender
            gender = f"`{info['gender']}`"

            # Yield acceptable voices
            if info[field] in values:
                yield (alias, region, gender)

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

    @commands.group(name='list', aliases=['l'])
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
            embed = Embed(
                title=":book: Voice Directory",
                description=(f":information_source: **Use** `{prefix}list "
                              "[Option]` **to see more filter options**"),
                colour=Colour.blue())

            # Generate information about possible subcommands
            embed.add_field(
                name="**Gender:**",
                value=f"`{prefix}list gender`")
            embed.add_field(
                name="**Language:**",
                value=f"`{prefix}list language`")

            await ctx.send(embed=embed)

    @list.command(name='gender', aliases=['gend'])
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
            genders = "`, `".join(gender for gender in supported_genders)

            embed = Embed(
                title=":book: Voice Directory - Gender",
                description=(f":information_source: **Use** `{prefix}list "
                              "gender [Gender]` **to display available "
                              "voices**"),
                colour=Colour.blue())
            embed.add_field(
                name=f"**Available Genders Options:**",
                value=f"`{genders}`")

        # Ensure that gender is supported
        elif await gender_is_valid(gender):
            # Create embed displaying all the available voices 
            # of a the particular gender
            page_number = 1
            embed = Embed(
                title=( ":book: Voice Directory - Gender - "
                       f"{gender.capitalize()}"),
                colour=Colour.blue())
            embed.set_footer(text=f"Page #{page_number}")

            field_index = 0
            for voice_info in self._voice_filter('gender', gender):
                # Check if the number of fields in the embed had exceed 24
                if(field_index >= self.MAX_EMBED_FIELDS):
                    await ctx.send(embed=embed)

                    field_index = 0
                    page_number += 1
                    embed = Embed(
                        title=(f":book: Voice Directory - Gender - "
                               f"{gender.capitalize()}"),
                        colour=Colour.blue())
                    embed.set_footer(text=f"Page #{page_number}")
                # Add voice to display
                embed.add_field(
                    name=f"{voice_info[0]}",
                    value=f"Region: {voice_info[1]}\nGender: {voice_info[2]}")
                field_index += 1

            if field_index > 3 and field_index % 3  == 2:
                embed.add_field(name="⠀", value="⠀")

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
            languages = "`, `".join(sorted(supported_languages.keys()))
            embed = Embed(
                title=":book: Voice Directory - Language",
                description=(f":information_source: **Use** `{prefix}list "
                              "language [Language]` **to display available "
                              "voices**"),
                colour=Colour.blue())
            embed.add_field(
                name="**Available Languages Options:**",
                value=f"`{languages}`")

        # Ensure that language is supported
        elif await language_is_valid(language):
            language = language.lower()
            lang_codes = supported_languages[language]

            # Create embed displaying all the available voices
            # of a the particular language
            page_num = 1
            embed = Embed(
                title=( ":book: Voice Directory - Language - "
                       f"{language.capitalize()}"),
                colour=Colour.blue())
            embed.set_footer(text=f"Page #{page_num}")

            field_index = 0
            for voice_info in self._voice_filter('lang_code', *lang_codes):
                # Check if the number of fields in the embed had exceed 24
                if(field_index >= self.MAX_EMBED_FIELDS):
                    await ctx.send(embed=embed)

                    field_index = 0
                    page_num += 1
                    embed = Embed(
                        title=( ":book: Voice Directory - Language - "
                               f"{language.capitalize()}"),
                        colour=Colour.blue())
                    embed.set_footer(text=f"Page #{page_num}")

                embed.add_field(name=f"{voice_info[0]}",
                                value=f"Region: {voice_info[1]}\n"
                                "Gender: {voice_info[2]}",
                                inline=True)
                field_index += 1

            if field_index > 3 and field_index % 3  == 2:
                embed.add_field(name="⠀", value="⠀")

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
        prefix = self.prefixes[ctx.guild]

        embed = Embed(
            title=":x: **Unsupported Gender**",
            description=(f"{error}\n\n:wrench: **Use the** `>list gender` "
                          "**command to view all supported genders**"),
            colour=Colour.red())
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
        prefix = self.prefixes[ctx.guild]

        embed = Embed(
            title=":x: **Unsupported Language**",
            description=(f"{error}\n\n:wrench: **Use the** `>list language` "
                          "**command to view all supported languages**"),
            colour=Colour.red())
        await ctx.send(embed=embed)



def setup(bot):
    """
    Adds Info Cog to bot.

    parameter:
        bot [Bot]: client object representing a Discord bot
    """
    bot.add_cog(Info(bot))
