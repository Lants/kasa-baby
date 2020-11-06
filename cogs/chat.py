import random, asyncio
import discord
from discord.ext import commands
from googletrans import Translator
import requests
from jservicepy import jService

# Cog for chat features

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.jService = jService()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "🇬🇧":
            await self.translateToEnglish(reaction, user)

    async def translateToEnglish(self, reaction, user):
        print(reaction.message.content)
        translated = self.translator.translate(reaction.message.content).text
        detected = self.translator.detect(reaction.message.content)
        print(detected.lang)
        if (reaction.count == 1 and not (detected.lang == "en") or user.id == self.bot.owner_id):
            chan = reaction.message.channel
            string = ("Translating %s's message from %s: %s") % (reaction.message.author.name, detected.lang.upper(), translated)
            await chan.send(string)
        

    #-------------------------------------COMMANDS-------------------------------------------
    
    # !eat <n>
    # Purge user's messages (bulk delete)
    @commands.command(name = "eat", description = "\"Feed me your yummy messages!\"\nDeletes a set number of your messages. Limit 7 per use. Only checks the last 30 messages.\nUsage: !eat <number of messages>")
    async def eat(self, ctx, n):
        """Deletes your own messages."""
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
    
    Lance has arbitrarily set 100 messages back as the maximum. If you want this larger, ask him!"""    
        
    # !eatAdmin <n> <all | @user1 @user2...>
    # Admin version of eat command. Allows targetting users and purging all
    # In: self, context, and a list of args:
        # Args: [<# of lines to delete> <Mention List | 'all'>]
    # Out: N/A
    @commands.command(name = "eatAdmin", description = eatAdminDesc)
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def eatAdmin(self, ctx, n, *, args: str):
        """!Eat, but with more power for admins."""
        n = int(n) + 1
        if n > 100:
            n = 100
        mentionList = ctx.message.mentions
        argsList = args.rstrip().lstrip().lower().split()

        if argsList[0] == 'all' and len(argsList) == 1:
            msgs = []
            async for msg in ctx.channel.history(limit = n):
                msgs.append(msg)
            await ctx.channel.delete_messages(msgs)
        else: # For every message within
            async for m in ctx.channel.history(limit = n):
                for targetUser in mentionList:
                    if targetUser.id == m.author.id:
                        await m.delete()
                        
        await ctx.send("I ate " + str(n) + " messages!", delete_after = 10)
        

    # !roll <n>
    # Random roll up to given number (inclusive)
    # In: self, ctx, n
    # Out: N/A
    @commands.command(name = "roll", description = "Random roll up to given number (inclusive). Usage: !roll <n>")
    async def roll(self, ctx, n):
        """Rolls a dice! Except the dice has infinite(?) sides..."""
        n = int(n)
        if n == 0:
            await ctx.send("If you have 0 friends, and try to choose a random friend, that doesn't change the fact that you still have 0 friends.")
        else:
            await ctx.send(random.randrange(n) + 1)


    # !xroll <x> <n>
    # Random roll, but x amount of times
    @commands.command(name = "xroll")
    async def xroll(self, ctx, x, n):
        """Same as roll, but does it 'x' amount of times."""
        x = int(x)
        n = int(n)
        if n == 0 or x == 0:
            await ctx.send("If you have 0 friends, and try to choose a random friend, that doesn't change the fact that you still have 0 friends.")
        else:
            out = ""
            while x > 0:
                x -= 1
                out = out + " " + str(random.randrange(n) + 1)
            await ctx.send(out)



    # !emoji
    # Prints ID of emoji sent
    @commands.command(name = "emoji", description = "Prints ID of given emoji")
    async def emoji(self, ctx):
        """Prints emojis for pasting into VSCode."""
        await asyncio.sleep(5)
        await ctx.send("```%s ```" % ctx.message.reactions)


    # !shittyinsult
    # Random Insult
    @commands.command(name = "shittyInsult")
    async def shittyinsult(self, ctx):
        """Generates a terrible insult"""
        # if len(args) == 0:
        #     url = "https://evilinsult.com/generate_insult.php?lang=%s" % args.rstrip().lstrip().split()[0].lower()
        # else:
        url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        response = requests.get(url).json()['insult']
        print(response)
        await ctx.send(response)

    #!dadjoke
    @commands.command(name = "dadJoke")
    async def dadjoke(self, ctx):
        """Retrieves a random dad joke from icanhazdadjoke.com"""
        await ctx.send(requests.get("https://icanhazdadjoke.com", headers={"Accept":"text/plain", "User-Agent":"Dummy Bot [Discord bot, personal project] (https://github.com/Lants/kasa-baby)"}).text)


    # !quiz
    # jeopardy??
    def isMessage(self, reaction, user):
        return reaction.message.author.id == user.id
    @commands.command(name = "quiz")
    async def quiz(self, ctx):
        """Uses jservice.io to fetch a jeopardy question. React to YOUR OWN message with any emoji to reveal answer"""
        q = self.jService.random()
        await asyncio.sleep(0.1)
        await ctx.send("%s for %d points: \"%s\"" % (q[0].category.title, q[0].value, q[0].question))
        try:
            reac = await self.bot.wait_for("reaction_add", timeout = 60, check = self.isMessage)
        except:
            pass
        finally:
            await ctx.send("Answer requested by %s: \"%s\"" % (reac[1].name, q[0].answer))

    #--------------------------------------COMMAND ERRORS-------------------------------------
    
    @eat.error
    async def eat_error(self, ctx, error):
        await ctx.send("\"wha?\"\nType <!help eat> for proper usage", delete_after = 10)
    
    # @eatAdmin.error
    # async def eatAdmin_error(self, ctx, error):
    #     await ctx.send("\"uh oh.. something went wrong!\"\nType <!help eatAdmin> for proper usage.\n")

    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.send("Usage: !roll <n>\n(Without the <>, and n is a positive integer)")

    @xroll.error
    async def xroll_error(self, ctx, error):
        await ctx.send("Usage: !xroll <x> <n> (Where x and n are both positive integers)")

def setup(bot):
    bot.add_cog(Chat(bot))