import asyncio
import functools
import itertools
import math
import random
import os

import discord
from discord.ext import commands
from discord import embeds
from async_timeout import timeout
from keep_alive import keep_alive

prefix = "%"
bot = commands.Bot(command_prefix=prefix)
my_secret = os.environ['TOKEN']
bot.remove_command('help')

@bot.command()
async def status(ctx):
  if ctx.author.id == 203346215423705089:
    await ctx.send('you get bitches')
  else:
    await ctx.send('you get no bitches')

#Help Command 
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.orange())
    
    embed.set_author(name='Help')
    embed.add_field(name='%help', value='Shows This Message', inline=False)
    embed.add_field(name='%snipe', value='Snipes the last deleted message',inline=False)
    #embed.add_field(name='%simonhelp',value='Summons The God Himself Simon', inline=False)
    embed.add_field(name='%say', value='Returns the string that you have inputted', inline=False)
    #embed.add_field(name='Confession', value='DM the bot and your messege will appear in the #confessions channels ', inline=False)
    await ctx.send(embed=embed)

#Primitive commands
@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(latency)

@bot.command()
async def say(ctx, *, content: str):
    await ctx.send(content)
    # await ctx.delete(ctx)

#Bad Words
with open("bad-words.txt") as file:
    bad_words = [bad_word.strip().lower() for bad_word in file.readlines()]
@bot.event
async def on_message(message):
    message_content = message.content.strip().lower()
    async for bad_word in bad_words:
        if bad_word in message:
            await bot.send_message(message.channel, "{}, your message has been censored.".format(message.author.mention))
            await bot.delete_message(message)

#Snipe Command
bot.sniped_messages = {}
@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)


#Confession Commands
msg_dump_channel = 856310321882595390
msg_log_channel = 856318481003053066

@bot.event
async def on_message(message: discord.Message):
    user = message.author
    channel = bot.get_channel(msg_dump_channel)
    otherchannel = bot.get_channel(msg_log_channel)
    if message.guild is None and not message.author.bot:
        await channel.send(message.content)
        await otherchannel.send(user)
        await otherchannel.send(message.content)
    await bot.process_commands(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ETWTheCatgirl#7427 is my developer "))
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

keep_alive()
bot.run(os.getenv("TOKEN"))
