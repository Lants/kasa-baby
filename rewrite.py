import discord
from discord.ext import commands
import json
import checks

with open('config.JSON') as config_file:
    config = json.load(config_file)

lance = 187028470998499340

description = '''Discord bot for KASA server. Imitates a baby. googoo gaga, bich\nUse !help <command> for instructions!'''

bot = commands.Bot(command_prefix = '!', description = description, case_insensitive = True, owner_id = lance)

#-------------Cogs-------------
# Cogs are an organizational system. This File is technically the bot,
# but all of its features are coded with cogs.
cogs = ['cogs.development',
        'cogs.chat',
        'cogs.hangman']



# On bot launch
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    for cog in cogs:
        bot.load_extension(cog)
    return
    
#---------------------------------------DEVELOPMENT TOOLS---------------------------------------------

################## THIS HAS BEEN MOVED TO "development.py" ###########################

# @bot.command(hidden = True)
# @commands.is_owner()
# async def unload(ctx, *, module: str):
#     """Unloads a module."""
#     try:
#         bot.unload_extension(module)
#     except Exception as e:
#         await ctx.send('\N{PISTOL}')
#         await ctx.send('{}: {}'.format(type(e).__name__, e))
#     else:
#         await cts.send('\N{OK HAND SIGN}')    

#---------------------------------------IGNORE-------------------------------------------------


bot.run(config['token'])