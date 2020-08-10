import random, asyncio
import discord
from discord.ext import commands

# Cog for chat features

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #-------------------------------------COMMANDS-------------------------------------------
    
    # !eat <n>
    # Purge user's messages (bulk delete)
    @commands.command(name = "eat", description = "\"Feed me your yummy messages!\"\nDeletes a set number of your messages. Limit 7 per use. Only checks the last 30 messages.\nUsage: !eat <number of messages>")
    async def eat(self, ctx, n):
        n = int(n) + 1
        if n > 8:
            n = 8
        i = 0
        userID = ctx.author.id
        async for m in ctx.channel.history(limit = 30):
            if userID == m.author.id:
                await m.delete()
                i = i + 1
            if i >= n:
                break
        await ctx.send("ate " + str(n - 1) + " messages! yummy!", delete_after = 4)
        
    eatAdminDesc = """\"This command is for 부모님 (parents) only!\"
    
    Admin only. 2 ways to use:
    1) [!eatAdmin <n> all] <-- deletes n messages from channel.
    2) [!eatAdmin <n> @user1 @user2 @user3...] <-- CHECKS n messages in channel history, deletes them if a matching user wrote it.
    
    Lance has arbitrarily set 150 messages back as the maximum. If you want this larger, ask him!"""    
        
    # !eatAdmin <n> <all | @user1 @user2...>
    # Admin version of eat command. Allows targetting users and purging all
    # In: self, context, and a list of args:
        # Args: [<# of lines to delete> <Mention List | 'all'>]
    # Out: N/A
    @commands.command(name = "eatAdmin", description = eatAdminDesc)
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def eatAdmin(self, ctx, n, *, args: str):
        n = int(n) + 1
        if n > 151:
            n = 151
        mentionList = ctx.message.mentions
        argsList = args.rstrip().lstrip().lower().split()

        if argsList[0] == 'all' and len(argsList) == 1:
            async for m in ctx.channel.history(limit = n):
                await m.delete()
        else: # For every message within
            async for m in ctx.channel.history(limit = n):
                for targetUser in mentionList:
                    if targetUser.id == m.author.id:
                        await m.delete()
                        
        await ctx.send("I ate " + str(n - 1) + " messages!", delete_after = 10)
        

    # !roll <n>
    # Random roll up to given number (inclusive)
    # In: self, ctx, n
    # Out: N/A
    @commands.command(name = "roll", description = "Random roll up to given number (inclusive). Usage: !roll <n>")
    async def roll(self, ctx, n):
        n = int(n)
        if n == 0:
            await ctx.send("If you have 0 friends, and try to choose a random friend, that doesn't change the fact that you still have 0 friends.")
        else:
            await ctx.send(random.randrange(n) + 1)


    # !emoji
    # Prints ID of emoji sent
    @commands.command(name = "emoji", description = "Prints ID of given emoji")
    async def emoji(self, ctx):
        await asyncio.sleep(5)
        await ctx.send("```%s ```" % ctx.message.reactions)

    #--------------------------------------COMMAND ERRORS-------------------------------------
    
    @eat.error
    async def eat_error(self, ctx, error):
        await ctx.send("\"wha?\"\nType <!help eat> for proper usage", delete_after = 10)
    
    @eatAdmin.error
    async def eatAdmin_error(self, ctx, error):
        await ctx.send("\"uh oh.. something went wrong!\"\nType <!help eatAdmin> for proper usage.\n")

    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.send("Usage: !roll <n>\n(Without the <>, and n is a positive integer)")

def setup(bot):
    bot.add_cog(Chat(bot))