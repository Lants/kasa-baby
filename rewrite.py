import discord
from discord.ext import commands
import random
import json
import checks

with open('config.JSON') as config_file:
    config = json.load(config_file)

lance = 187028470998499340

description = '''Discord bot for KASA server. Imitates a baby. googoo gaga, bich'''

bot = commands.Bot(command_prefix = '!', description = description, case_insensitive = True, owner_id = lance)

#-------------Cogs-------------
# Cogs are an organizational system
cogs = ['cogs.development']


# On bot launch
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    for cog in cogs:
        bot.load_extension(cog)
    return
    
    

#---------------------------------------IGNORE-------------------------------------------------


bot.run(config['token'])