import discord
from discord.ext import commands
import random
import json

with open('config.json') as config_file:
    config = json.load(config_file)

description = '''Discord bot for KASA server. Imitates a baby. googoo gaga, bich'''

bot = commands.Bot(command_prefix = '!', description = description, case_insensitive = True)




# On bot launch
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    
# On bot received message
@bot.event
async def on_message(message):
    print('received: ' + message.content)
    
    
    
    # Run any commands that were called
    await bot.process_commands(message)
    
    
#------------------------------------------COMMANDS------------------------------------------

# Close connection to Discord
# note: ctx is Context, see Discord.py docs for more details.
@bot.command()
async def close(ctx):
    print(ctx.author)
    
# Echo back input. Used for testing.
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------IGNORE-------------------------------------------------


bot.run(config.token)