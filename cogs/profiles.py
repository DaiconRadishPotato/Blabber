# profiles.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 5/4/2020
# Python Version: 3.8.1
# License: MIT License

import json

from discord.ext import commands
from discord import Embed, Colour
from blabber.cache import VoiceProfileCache


class Profiles(commands.Cog):
    """
    Profiles Cog Object that is a collection of commands for managing a user's
    voice profiles

    parameters:
        bot [discord.Bot]: discord Bot object
        aliases [set]: set object of string alias/voice names
    """

    def __init__(self, bot):
        self.DEFAULT_VOICE = (
            'voice_1',
            'de-DE-Standard-F',
            'FEMALE',
            'de',
            'de-DE'
        )
        self.bot = bot
        self.vpc = VoiceProfileCache()

        with open(r'./blabber/data.json', 'r') as f:
            data = json.load(f)
            self._aliases = data['voice_info']

    @commands.command(name='voice', aliases=['v'])
    async def set_voice(self, ctx, *, alias):
        """
        Sets up and updates a user voice profile in the database. Displays a
        message to user if set was successful or failed.

        parameter:
            ctx [commands.Context]: discord Contxt object
            alias [str]: string representing a specific alias
        raises:
            MissingRequiredArgument: an alias was not passed as an argument
        """
        if self._aliases[alias] is not None:
            self.vpc[(ctx.author, ctx.channel)] = alias

        await ctx.send(f":white_check_mark: **The new voice is **'{alias}'")

    async def _get_voice(self, user, channel):
        """
        Prints current users current voice profile.

        parameter:
            user [User]: discord User object
            channel_id [Channel]: discord Channel Object
        returns:
            voice [tuple]: tuple of voice information from database
        """
        voice = self.vpc[(user, channel)]
        return voice

    @set_voice.error
    async def set_voice_error(self, ctx, error):
        """
        Sends informational embed to be displayed if set voice command
        is being missing arguments

        parameters:
            ctx [commands.Context]: discord Context object
            error [Error]: general Error object
        """
        if isinstance(error, commands.MissingRequiredArgument):
            voice = (await self._get_voice(ctx.author, ctx.channel))[0]
            prefix = await self.bot.get_cog("Settings")._get_prefix(ctx.guild)
            member = ctx.message.author

            embed = Embed(
                title="Blabber Voice",
                description="Changes the voice used to send messages in "
                "Blabber bot. You can also use the bot by @mentioning it "
                "instead of using the prefix. See list for all supported "
                "voices",
                colour=Colour.blue())

            embed.add_field(name=f"{member}'s current Voice:",
                            value=f"`{voice}`")

            embed.add_field(name="Update Voice:",
                            value=f"`{prefix}v [new voice]`")

            await ctx.send(embed=embed)
        elif isinstance(error.original, KeyError):
            embed = Embed(title="Blabber Voice - Setting Voice",
                          colour=Colour.blue())

            embed.add_field(name="Input Voice:",
                            value=f"`{ctx.args[2]}` is not available.")

            embed.add_field(name='To list all available voice options:',
                            value=f"`{prefix}list`")

            await ctx.send(embed=embed)



def setup(bot):
    """
    Adds Settings Cog to bot.

    parameter:
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Profiles(bot))
