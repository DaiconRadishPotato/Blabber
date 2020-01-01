#Blabber
'''Created by:
Fanny Avila (Fa-Avila)
Marcos Avila (DaiconV),
Jacky Zhang (jackyeightzhang)'''

import os
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('discord_token')

bot = commands.Bot(command_prefix='>')

#check to see if the bot is functional
@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('greeting::hello invoked')
    await bot.close()

#connect bot to the voice chat that the user is in
@bot.command(name='connect')
async def connectToVC(ctx):
    voiceChannel = ctx.message.author.voice.channel
    await ctx.send(f'connectToVC::TestDiscodPyBot connecting to {voiceChannel.name}')
    await voiceChannel.connect()

#disconnect bot from voice chat that user is in
@bot.command(name='disconnect')
async def disconnectFromVC(ctx):
    voiceClient = ctx.voice_client
    await ctx.send(f'disconnectFromVC::TestDiscodPyBot disconnecting from {voiceClient.channel}')
    await voiceClient.disconnect()
    
bot.run(TOKEN)
