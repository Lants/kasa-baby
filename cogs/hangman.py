import discord
from discord.ext import commands
import os.path
import random
import linecache
import asyncio


class Hangman(commands.Cog):

    def resetHangman(self):
        self.__isPlaying = False
        self.__guess = ''

    def __init__(self, bot):
        self.bot=bot
        self.__file = os.path.join(os.path.dirname(__file__), os.pardir, 'gameref/wordlist.txt')
        self.__maxline = 69340
        self.resetHangman()

    @commands.Cog.listener()
    async def on_ready(self):
        print('loaded cog: {self.__name__}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(self.__guess) == 0 and len(message.content) == 1 and self.__isPlaying:
            self.__guess = message.content



    #------------------------------------------COMMANDS------------------------------------------
    # !hangman
    # Plays hangman
    @commands.command(name = 'hangman', description = 'Play hangman!')
    async def hangman(self, ctx):
        # Setup
        rand = random.randint(0, self.__maxline)
        word = list(linecache.getline(self.__file, rand).strip())
        status = word.copy()
        i = 0
        self.__isPlaying = True

        await ctx.send(word)
        for letter in word:
            if letter != '-':
                status[i] = '\_'
            else:
                status[i] = '-'
            i = i + 1
        await ctx.send(' '.join(status))

        # Guess phase
        while self.__isPlaying and '\_' in status:
            try:
                await self.bot.wait_for('message', timeout = 60)
                if len(self.__guess) == 1:
                    i = 0
                    for letter in word:
                        print(i)
                        if letter == self.__guess:
                            status[i] = self.__guess
                        else:
                            # Implement incorrect guesses here
                            pass
                        i = i + 1
                    self.__guess = ''
                    await ctx.send(' '.join(status))
                else:
                    continue
                    
            except Exception as e:
                self.resetHangman()
                if isinstance(e, asyncio.TimeoutError):
                    await ctx.send("Timed out, quitting hangman.")
                else:
                    await ctx.send(e)
                return


def setup(bot):
    bot.add_cog(Hangman(bot))