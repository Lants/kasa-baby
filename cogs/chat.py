import discord
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #-------------------------------------COMMANDS-------------------------------------------
    # Purge user's messages (bulk delete)
    @commands.command(name = "eat", description = "Feed me your yummy messages!\nDeletes a set number of your messages. Limit 7 per use. Only checks the last 30 messages.\nUsage: !eat <number of messages>")
    async def eat(self, ctx, n):
        n = int(n) + 1
        if n > 8:
            n = 8
        N = n
        i = 0
        userID = ctx.author.id
        async for m in ctx.channel.history(limit = 30):
            if userID == m.author.id:
                await m.delete()
                i = i + 1
            if i >= n:
                break
        await ctx.send("ate " + str(N) + " messages! yummy!", delete_after = 4)
        
    # Admin version of eat command. Allows targetting users and purging all
    # In: self, context, and a list of args:
    # Args: [<# of lines to delete> <Mention List | 'all'>]
    #--------------------------------------COMMAND ERRORS-------------------------------------
    
    @eat.error
    async def eat_error(self, ctx, error):
        await ctx.send("wha?\nUsage: !eat #", delete_after = 10)

def setup(bot):
    bot.add_cog(Chat(bot))