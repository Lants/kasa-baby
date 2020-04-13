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




# On bot launch
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    
# On bot received message
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    print('received: ' + message.content)
    
    
    
    # Run any commands that were called
    await bot.process_commands(message)
    
    
#------------------------------------------COMMANDS------------------------------------------

# Close connection to Discord
# note: ctx is Context, see Discord.py docs for more details.
@bot.command()
@commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
async def sleep(ctx):
    if random.random() < .5:
        await ctx.channel.send("nighty night! I go sleep now " + str(ctx.author.mention))
    else:
        await ctx.channel.send("aw, it's not my bedtime yet " + str(ctx.author.mention) + "! fine.. goodnight!")
    await ctx.bot.logout()
    
# Echo back input. Used for testing.
@bot.command()
@commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
async def echo(ctx, *, message: str):
    await ctx.send(message)







#-------------------------------------------COMMAND ERROR HANDLING-----------------------------------------------    
@echo.error
async def echo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("uhh.. ur not good enough to do this sorry")
    
    
    
    
    
    
    
    
    
    
#---------------------------------------IGNORE-------------------------------------------------


bot.run(config['token'])