# Developer commands and tools for kasa baby bot

from discord.ext import commands
import random

class Development(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    #------------------------------------------COMMANDS------------------------------------------

    # Close connection to Discord
    @commands.command(name = "sleep", description = "Put me to sleep!")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def sleep(self, ctx):
        if random.random() < .5:
            await ctx.channel.send("nighty night! I go sleep now " + str(ctx.author.mention))
        else:
            await ctx.channel.send("aw, it's not my bedtime yet " + str(ctx.author.mention) + "! fine.. goodnight!")
        await ctx.bot.logout()
        
    # Echo back input. Used for testing.
    @commands.command(name = "echo", description = "Echoes back input. Used for testing.")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def echo(self, ctx, *, args: str):
        await ctx.send(args)





    #-------------------------------------------COMMAND ERROR HANDLING-----------------------------------------------    
    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("uhh.. ur not good enough to do this sorry")
        
    @sleep.error    
    async def sleep_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Only my parents can make make me go to bed! (Admins only dummy)")
        
        
        
def setup(bot):
    bot.add_cog(Development(bot))        
        
        