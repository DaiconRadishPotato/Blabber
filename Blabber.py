#Blabber.py
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

#in the future add a help function

#command for testing purposes, to check to see if the bot is functional
@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Blabber::hello invoked')
    await bot.close()

#command for testing purposes, to check to see if the bot prints out the username (name) and nickname(display name)
@bot.command(name='user')
async def user(ctx):
    await ctx.send(f'Blabber::user hello user {ctx.author.name} or should I say {ctx.author.display_name}')
    await bot.close()
    
#command to disconnect bot from voice chat that user is in
@bot.command(name='disconnect')
async def disconnectFromVC(ctx):
    if ctx.voice_client == None:
        await ctx.send('Blabber::disconnectFromVC Blabber is not connected')
    elif len(ctx.voice_client.channel.members) == 1 or ctx.author in ctx.voice_client.channel.members:
        voiceClient = ctx.voice_client
        await ctx.send(f'Blabber::disconnectFromVC disconnecting from {voiceClient.channel}')
        await voiceClient.disconnect()
    else:
        await ctx.send('Blabber::disconnectFromVC You need to be in a voice channel to use this command.')

#command to connect bot to the voice chat that the user is in
@bot.command(name='connect')
async def connectToVC(ctx):
    if ctx.author.voice.channel == None:
        await ctx.send('Blabber::connectToVC You need to be in a voice channel to use this command.') 
    elif ctx.voice_client == None:
        voiceChannel = ctx.author.voice.channel
        await ctx.send(f'Blabber::connectToVC connecting to {voiceChannel.name}')
        await voiceChannel.connect()
    elif ctx.voice_client.channel == ctx.author.voice.channel:
        await ctx.send(f'Blabber::connectToVC already connected to {voiceChannel.name}')
    elif len(ctx.voice_client.channel.members) == 1:
        await ctx.send(f'Blabber::connectToVC swaping from {ctx.voice_client.channel} to {ctx.author.voice.channel.name}')
        await ctx.voice_client.move_to(ctx.author.voice.channel)

bot.run(TOKEN)
