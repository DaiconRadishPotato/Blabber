# info.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 4/15/2020
# Python Version: 3.8.1
# License: MIT License

import json

from discord.ext import commands
from discord import Embed, Colour
from blabber.filter_services import FilterServices

class Info(commands.Cog):
    """
    Collection of commands for displaying information about Blabber for each 
    guild.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot
        self.MAX_EMBED_FIELDS = 25
        with open(r'./blabber/genders.json', 'r') as gender_f:
            self._genders = json.load(gender_f)
        with open(r'./blabber/language_codes.json', 'r') as lang_code_f:
            self._languages = json.load(lang_code_f)

    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        Prints out description of all available commands for Blabber to the 
        text channel where the bot was invoked.

        paramters:
            ctx [commands.Context]: discord Context object
        """
        prefix = await self.bot.get_cog("Settings")._get_prefix(ctx.guild.id)
        embed = Embed(title="Help Directory", 
        description="",
        colour=Colour.gold())

        embed.add_field(name=f"`{prefix}help` or `{prefix}h`",
        value=f"Displays this message.",
        inline=False)

        embed.add_field(name=f"`{prefix}connect` or `{prefix}c`",
        value='Connect Blabber to the voice channel you\'re in',
        inline=False)
        
        embed.add_field(name=f"`{prefix}disconnect` or `{prefix}dc`",
        value='Disconnect Blabber from its voice channel',
        inline=False)

        embed.add_field(name=f"`{prefix}say [message]` or `{prefix}s "
        "[message]`",
        value="Tell Blabber to say something. If Blabber is not in the same "
        "voice channel, then it will join.",
        inline=False)

        embed.add_field(name=f"`{prefix}settings` or `{prefix}s`", 
        value="Displays settings menu, which allows the certain users to "
        "change Blabber Bot settings such as the prefix",
        inline=False)
        
        embed.add_field(name=f"`{prefix}settings prefix` or `{prefix}settings "
        "p`", value="Displays current guild prefix.",
        inline=False)
        
        embed.add_field(name=f"`{prefix}list` or `{prefix}l`", 
        value="Displays the Voice Directory and voices.",
        inline=False)
        
        await ctx.send(embed=embed)
        
    @commands.group(name='list', aliases=['l','ls'])
    async def list_available_voices(self, ctx):
        """
        Displays list voice options for the user to either display a filter 
        version or all their voice options.

        parameters:
            ctx [commands.Context]: discord Context object
        """
        if ctx.invoked_subcommand is None:
            prefix = await self.bot.get_cog(
                "Settings")._get_prefix(ctx.guild.id)

            embed = Embed(title="Voice Directory", description="Use the "
            f"command {prefix}list [option] to filter the available voices.",
            colour=Colour.green())

            embed.add_field(name="all", value=f"`{prefix}list all`", 
            inline=False)
            
            embed.add_field(name="gender", 
            value=f"`{prefix}list gender [male, female, neutral]`", 
            inline=False)
            
            embed.add_field(name="language", 
            value=f"`{prefix}list language [language]`", inline=False)
            await ctx.send(embed=embed)

    @list_available_voices.command(name='gender', aliases=['g'])
    async def voice_gender_filter(self, ctx, gender: str):
        """
        Subcommand of list that displays all available voices that have the 
        specified gender.
        If a gender is not specified, then display available genders.

        parameters:
            ctx [commands.Context]: discord Context object
            gender [str]: string object used to represent the gender to filter
        """
        if self._genders[gender]:
            fs = FilterServices()
            records = fs.filter_by_gender(self._genders[gender])
            if not records:
                await ctx.send("database has a problem")
            else:
                page_num = 1
                embed = Embed(title="Voice Directory - List of Voices - Gender"
                " Filter - Page "+ str(page_num),
                colour=Colour.green())
                for record_num in range(len(records)):
                    alias = records[record_num]
                    if (record_num % (self.MAX_EMBED_FIELDS+1)
                    == self.MAX_EMBED_FIELDS):
                        await ctx.send(embed=embed)
                        page_num += 1
                        embed = Embed(title="Voice Directory - List of Voices "
                        "- Gender Filter - Page "+ str(page_num), 
                        colour=Colour.green())
                    embed.add_field(name=f"{alias[0]}", 
                    value=f"language: {alias[1]}\ngender: {alias[2]}", 
                    inline=True)
                await ctx.send(embed=embed)

    @list_available_voices.command(name='language', aliases=['lang'])
    async def voice_language_filter(self, ctx, language:str):
        """
        Subcommand of list that displays all available voices that have the 
        specified language.
        If a language is not specified, then display available language.
         
        parameters:
            ctx [commands.Context]: discord Context object
            language [str]: string object used to represent the gender to filter
        """
        if(self._languages[language]):
            fs = FilterServices()
            records = fs.filter_by_lang(self._languages[language])

            if not records:
                await ctx.send("database has a problem")
            else:
                page_num = 1
                embed = Embed(title="Voice Directory - List of Voices - "
                "Language Filter - Page " + str(page_num), 
                colour=Colour.green())
                for record_num in range(len(records)):
                    alias = records[record_num]
                    if (record_num % (self.MAX_EMBED_FIELDS+1)
                    == self.MAX_EMBED_FIELDS):
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
        embed = Embed(title="Voice Directory - List of Voices - Gender"
            " Filter", colour=Colour.green())
        prefix = await self.bot.get_cog("Settings"
            )._get_prefix(ctx.guild.id)
        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name="show male voices only", 
            value=f"{prefix}list gender male")
            embed.add_field(name="show female voices only", 
            value=f"{prefix}list gender female")
            embed.add_field(name="show neutral voices", 
            value=f"{prefix}list gender neutral")
            await ctx.send(embed=embed)
        elif isinstance(error.original, KeyError):
            embed.add_field(name="Input Gender:", 
            value=f"`{ctx.args[2]}` is not available.")
            embed.add_field(name="Available Genders:", 
            value="`male`, `female`, and `neutral`")
            await ctx.send(embed=embed)

    @voice_language_filter.error
    async def voice_language_filter_error(self, ctx, error):
        embed = Embed(title="Voice Directory - List of Voices - "
            "Language Filter", colour=Colour.green())
        prefix = await self.bot.get_cog("Settings"
            )._get_prefix(ctx.guild.id)
        if isinstance(error, commands.MissingRequiredArgument):
            # available_voices = db.get_voice_profile_lang()
            # for alias in available_voices:
            #     embed.add_field(name=f"`{alias}`", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error.original, KeyError):
            embed.add_field(name="Input Language:", 
            value=f"`{ctx.args[2]}` is not available.")
            embed.add_field(name="To get available languages use:", 
            value=f"`{prefix}list lang`")
            await ctx.send(embed=embed)


def setup(bot):
    """
    Removes templated help function and adds Help Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Info(bot))
