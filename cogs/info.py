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
    Collection of commands for displaying information about Blabber.

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
        Displays descriptions of all available commands for Blabber.

        paramters:
            ctx [Context]: context object representing command invocation
        """
        embed = Embed(
            title=":blue_book: **List of Commands**",
            colour=Colour.blue())
        prefix = self.prefixes[ctx.guild]

        # Generate information for voice.py commands
        embed.add_field(
            name="**Connect:**",
            value=(f"`{prefix}connect`, `{prefix}c`\n"
                    "Summon Blabber to your voice channel"),
            inline=False)
        embed.add_field(
            name="**Disconnect:**",
            value=(f"`{prefix}disconnect`, `{prefix}dc`\n"
                    "Dismiss Blabber from voice channel"),
            inline=False)
        embed.add_field(
            name="**Say:**",
            value=(f"`{prefix}say [Message]`, `{prefix}s [Message]`\n"
                    "Recite a message to your voice channel"),
            inline=False)

        # Generate information for info.py commands
        embed.add_field(
            name="**List:**",
            value=(f"`{prefix}list`, `{prefix}l`\n"
                    "Display supported TTS narrator voices"),
            inline=False)

        # Generate information for profiles.py commands
        embed.add_field(
            name="**Voice:**",
            value=(f"`{prefix}voice`, `{prefix}v`\n"
                    "Display and change your TTS narrator voice"),
            inline=False)

        # Generate information for settings.py commands
        embed.add_field(
            name="**Settings:**",
            value=(f"`{prefix}settings`, `{prefix}set`\n"
                    "Display and change server settings for Blabber"),
            inline=False)

        # Generate information for roles.py commands
        embed.add_field(
            name="**Give Blabby:**",
            value=(f"`{prefix}giveblabby [Member]`, `{prefix}gb [Member]`\n"
                    "Assigns `Blabby` role to a server member"),
            inline=False)

        await ctx.send(embed=embed)

    @commands.group(name='list', aliases=['l'])
    async def list(self, ctx):
        """
        Displays options for filtering list of TTS narrator voices.

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
                value=f"`{prefix}list gender`,\n`{prefix}list gend`")
            embed.add_field(
                name="**Language:**",
                value=f"`{prefix}list language`,\n`{prefix}list lang`")

            await ctx.send(embed=embed)

    @list.command(name='gender', aliases=['gend'])
    async def list_gender(self, ctx, gender: str=''):
        """
        Displays TTS narrator voices filtered by gender.

        parameters:
            ctx [Context]: context object representing command invocation
            gender  [str] (default=''): gender to filter by
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
            field_index = 0
            page_number = 1

            # Generate embed page
            embed = Embed(
                title=( ":book: Voice Directory - Gender - "
                       f"{gender.capitalize()}"),
                colour=Colour.blue())
            embed.set_footer(text=f"Page #{page_number}")

            for voice_info in self._voice_filter('gender', gender):
                # Check if the number of fields exceeds embed page limit
                if (field_index >= self.MAX_EMBED_FIELDS):
                    field_index = 0
                    page_number += 1

                    # Send old embed page
                    await ctx.send(embed=embed)

                    # Generate new embed page
                    embed = Embed(
                        title=(f":book: Voice Directory - Gender - "
                               f"{gender.capitalize()}"),
                        colour=Colour.blue())
                    embed.set_footer(text=f"Page #{page_number}")

                # Add voice to embed
                embed.add_field(
                    name=f"{voice_info[0]}",
                    value=f"Region: {voice_info[1]}\nGender: {voice_info[2]}")

                field_index += 1

            # Add padding field if needed
            if field_index > 3 and field_index % 3 == 2:
                embed.add_field(name="⠀", value="⠀")

        await ctx.send(embed=embed)

    @list.command(name='language', aliases=['lang'])
    async def list_language(self, ctx, language: str=''):
        """
        Displays TTS narrator voices filtered by language.

        parameters:
            ctx  [Context]: context object representing command invocation
            language [str] (default=''): language to filter by
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

            field_index = 0
            page_number = 1

            # Generate embed page
            embed = Embed(
                title=( ":book: Voice Directory - Language - "
                       f"{language.capitalize()}"),
                colour=Colour.blue())
            embed.set_footer(text=f"Page #{page_number}")

            for voice_info in self._voice_filter('lang_code', *lang_codes):
                # Check if the number of fields exceeds embed page limit
                if (field_index >= self.MAX_EMBED_FIELDS):
                    field_index = 0
                    page_number += 1

                    # Send old embed page
                    await ctx.send(embed=embed)

                    # Generate new embed page
                    embed = Embed(
                        title=( ":book: Voice Directory - Language - "
                               f"{language.capitalize()}"),
                        colour=Colour.blue())
                    embed.set_footer(text=f"Page #{page_number}")

                # Add voice to embed
                embed.add_field(
                    name=f"{voice_info[0]}",
                    value=f"Region: {voice_info[1]}\nGender: {voice_info[2]}")

                field_index += 1

            # Add padding field if needed
            if field_index > 3 and field_index % 3 == 2:
                embed.add_field(name="⠀", value="⠀")

        await ctx.send(embed=embed)

    @list_gender.error
    async def list_gender_error(self, ctx, error):
        """
        Local error handler for subcommand list gender.

        parameters:
            ctx     [Context]: context object produced by a command invocation
            error [Exception]: error object thrown by command function
        """
        prefix = self.prefixes[ctx.guild]

        embed = Embed(
            title=":x: **Unsupported Gender**",
            description=(f"{error}\n\n:wrench: **Use** `>list gender` **to "
                          "view all supported genders**"),
            colour=Colour.red())
        await ctx.send(embed=embed)

    @list_language.error
    async def list_language_error(self, ctx, error):
        """
        Local error handler for subcommand list language.

        parameters:
            ctx     [Context]: context object produced by a command invocation
            error [Exception]: error object thrown by command function
        """
        prefix = self.prefixes[ctx.guild]

        embed = Embed(
            title=":x: **Unsupported Language**",
            description=(f"{error}\n\n:wrench: **Use** `>list language` **to "
                          "view all supported languages**"),
            colour=Colour.red())
        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Info Cog to bot.

    parameter:
        bot [Bot]: client object representing a Discord bot
    """
    bot.add_cog(Info(bot))
