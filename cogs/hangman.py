import discord
from discord.ext import commands
import os.path
import random
import linecache
import asyncio
import gameref.hangmanArt as hArt


class Hangman(commands.Cog):

    def resetHangman(self):
        self.__isPlaying = False
        self.__guess = ''
        self.__file = None
        self.wrongLim = 0
        self.__art = 0
        self.__guessed = []

    def __init__(self, bot):
        self.bot = bot
        self.__maxline = 69340
        self.resetHangman()
        self.__art = 0
        self.__guessed = []

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
        self.__file = os.path.join(os.path.dirname(__file__), os.pardir, 'gameref/wordlist.txt')
        word = list(linecache.getline(self.__file, rand).strip())
        status = word.copy()
        i = 0
        self.__wrongLim = len(status) + 4
        print("Hangman wrong limit: " + str(self.__wrongLim))
        wrongCount = 0
        self.__isPlaying = True
        self.__file = None
        artInterval = self.__wrongLim / 7



        # await ctx.send(word)
        for letter in word:
            if letter != '-':
                status[i] = '\_'
            else:
                status[i] = '-'
            i = i + 1
        await ctx.send("Attempts: " + str(self.__wrongLim))
        await ctx.send(' '.join(status))

        # Guess phase
        while self.__isPlaying and '\_' in status:
            try:
                await self.bot.wait_for('message', timeout = 60)
                if len(self.__guess) == 1:
                    i = 0
                    incorrect = True
                    if self.__guess in word:
                        for letter in word:
                            if letter == self.__guess:
                                status[i] = self.__guess
                                incorrect = False
                            i = i + 1

                    # Implement incorrect guesses here
                    print(self.__guess + " " + str(self.__guessed))
                    print(bool(self.__guess not in self.__guessed))
                    if incorrect and (self.__guess not in self.__guessed):
                        print("entered")
                        wrongCount = wrongCount + 1
                        if wrongCount >= self.__wrongLim:
                            await ctx.send("You hung a man... oh no..")
                            await ctx.send(word)
                            self.resetHangman()
                    self.__guessed.append(self.__guess)
                    self.__guess = ''
                    if self.__isPlaying:
                        await ctx.send(hArt.artChooser(int(wrongCount / artInterval)))
                        await ctx.send("Remaining attempts: " + str(self.__wrongLim - wrongCount) + "\n" + ' '.join(status))
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