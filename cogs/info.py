# info.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 4/28/2020
# Python Version: 3.8.1
# License: MIT License

import json

from discord.ext import commands
from discord import Embed, Colour


class Info(commands.Cog):
    """
    Collection of commands for displaying information about Blabber Bot for the
    particular guild.

    attributes:
        bot [discord.Bot]: discord Bot object
    """

    def __init__(self, bot):
        self.bot = bot
        self.MAX_EMBED_FIELDS = 25
        self.LANG_CODE_INDEX = 0
        self.LANG_INDEX = 1
        with open(r'./blabber/data.json', 'r') as f:
            data = json.load(f)
            self._languages_map = data['languages']
            self._genders_map = data['genders']
            self._voices_map = data['voice_info']

    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        Prints out description of all available commands for Blabber to the
        text channel where the bot was invoked.

        paramters:
            ctx [commands.Context]: discord Context object
        """
        prefix = await self.bot.get_cog("Settings")._get_prefix(ctx.guild)
        embed = Embed(title="Help Directory",
                      description="",
                      colour=Colour.gold())

        embed.add_field(name=f"`{prefix}help` or `{prefix}h`",
                        value=f"Displays this message.",
                        inline=False)

        embed.add_field(name=f"`{prefix}voice [alias]` or `{prefix}v [alias]`",
                        value="Set a specific voice for your say commands "
                        "unique to the guild",
                        inline=False)

        embed.add_field(name=f"`{prefix}disconnect` or `{prefix}dc`",
                        value="Disconnect Blabber from its voice channel",
                        inline=False)

        embed.add_field(name=f"`{prefix}say [message]` or `{prefix}s "
                        "[message]`",
                        value="Tell Blabber to say something. If Blabber is "
                        "not in the same voice channel, then it will join.",
                        inline=False)

        embed.add_field(name=f"`{prefix}list` or `{prefix}l`",
                        value="Displays the Voice Directory and voices.",
                        inline=False)

        embed.add_field(name=f"`{prefix}settings`",
                        value="Displays settings menu, which allows the "
                        "certain users to change Blabber Bot settings such as "
                        "the prefix",
                        inline=False)

        embed.add_field(name=f"`{prefix}settings prefix` or `{prefix}settings "
                        "p`", value="Displays current guild prefix.",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.group(name='list', aliases=['l', 'ls'])
    async def list_available_voices(self, ctx):
        """
        Displays list voice options for the user to display a filter
        version based on either gender or language.

        parameters:
            ctx [commands.Context]: discord Context object
        """
        if ctx.invoked_subcommand is None:
            prefix = await self.bot.get_cog("Settings")._get_prefix(ctx.guild)

            embed = Embed(title="Voice Directory", description="Use the "
                          f"command `{prefix}list [option]`"
                          "to show filter options.",
                          colour=Colour.green())

            embed.add_field(name="Gender",
                            value=f"`{prefix}list gender`",
                            inline=False)

            embed.add_field(name="Language",
                            value=f"`{prefix}list language`",
                            inline=False)

            await ctx.send(embed=embed)

    @list_available_voices.command(name='gender', aliases=['g'])
    async def voice_gender_filter(self, ctx, gender: str):
        """
        Subcommand of list that displays all available voices that have the
        specified gender.

        parameters:
            ctx [commands.Context]: discord Context object
            gender [str]: string object used to represent the gender to filter
        raises:
            MissingRequiredArgument: gender was not passed as an argument
            KeyError: gender was not avaiable or there was incorrectly inputted
        """
        records = [
            (voice, info['language'], info['gender'])
            for voice, info in self._voices_map.items()
            if info['gender'] == self._genders_map[gender]
        ]
        page_num = 1
        embed = Embed(title="Voice Directory - List of Voices"
                      " - Gender Filter - Page " + str(page_num),
                      colour=Colour.green())

        for record_num in range(len(records)):
            alias = records[record_num]

            if (record_num % (self.MAX_EMBED_FIELDS + 1) ==
                    self.MAX_EMBED_FIELDS):
                await ctx.send(embed=embed)
                page_num += 1
                embed = Embed(title="Voice Directory - List of Voices"
                              " - Gender Filter - Page " + str(page_num),
                              colour=Colour.green())

            embed.add_field(name=f"{alias[0]}",
                            value=f"language: {alias[1]}\ngender: {alias[2]}",
                            inline=True)

        await ctx.send(embed=embed)

    @list_available_voices.command(name='language', aliases=['lang'])
    async def voice_language_filter(self, ctx, language: str):
        """
        Subcommand of list that displays all available voices that have the
        specified language.

        parameters:
            ctx [commands.Context]: discord Context object
            language [str]: string object used to represent the gender to
            filter
        raises:
            MissingRequiredArgument: language was not passed as an argument
            KeyError: language was not avaiable or was incorrectly inputted
        """
        language = language.lower()
        records = [
            (voice, info['language'], info['gender'])
            for voice, info in self._voices_map.items()
            if info['language'] ==
            self._languages_map[language][self.LANG_CODE_INDEX]
        ]
        page_num = 1
        embed = Embed(title="Voice Directory - List of Voices - "
                      "Language Filter - Page " + str(page_num),
                      colour=Colour.green())

        for record_num in range(len(records)):
            alias = records[record_num]

            if (record_num % (self.MAX_EMBED_FIELDS + 1) ==
                    self.MAX_EMBED_FIELDS):
                await ctx.send(embed=embed)
                page_num += 1
                embed = Embed(title="Voice Directory - List of Voices"
                              " - Language Filter - Page " + str(page_num),
                              colour=Colour.green())

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
            ctx [commands.Context]: discord Context object
            error [Error]: general Error object
        """
        embed = Embed(title="Voice Directory - List of Voices"
                      " - Gender Filter Options", colour=Colour.green())
        prefix = await self.bot.get_cog("Settings")._get_prefix(ctx.guild)

        available_genders = ", ".join(gender
                                      for gender in self._genders_map.keys())

        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name=f"Available Genders Options:",
                            value=f"`{available_genders}`")

            embed.add_field(name="To list voices filtered by a gender:",
                            value=f"`{prefix}list gender [gender_option]`")

            await ctx.send(embed=embed)

        elif isinstance(error.original, KeyError):
            embed.add_field(name="Input Gender:",
                            value=f"`{ctx.args[2]}` is not available.")

            embed.add_field(name=f"Available Genders Options:",
                            value=f"`{available_genders}`")
            await ctx.send(embed=embed)

    @voice_language_filter.error
    async def voice_language_filter_error(self, ctx, error):
        """
        Local error handler for subcommand list language.
        If no language argument, display how to invoke command.
        If key error, display the invalid argument and valid languages.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Error]: general Error object
        """
        embed = Embed(title="Voice Directory - List of Voices - "
                      "Language Filter Menu", colour=Colour.green())
        prefix = await self.bot.get_cog("Settings")._get_prefix(ctx.guild)

        available_languages = ", ".join(sorted(
            lang_list[self.LANG_INDEX]
            for lang_list in self._languages_map.values()))

        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name='Available Languages Options:',
                            value=f"`{available_languages}`")

            embed.add_field(name="To list voices filtered by a language:",
                            value=f"`{prefix}list lang [language_option]`")

            await ctx.send(embed=embed)
        elif isinstance(error.original, KeyError):
            embed.add_field(name="Input Language:",
                            value=f"`{ctx.args[2]}` is not available.")

            embed.add_field(name='Available Languages Options:',
                            value=f"`{available_languages}`")

            await ctx.send(embed=embed)


def setup(bot):
    """
    Removes templated help function and adds Help Cog to bot.

    parameter:
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Info(bot))
