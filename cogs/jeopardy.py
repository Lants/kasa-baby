from discord.ext import commands

class Jeopardy(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if len(self.__guess) == 0 and len(message.content) == 1 and self.__isPlaying:
            self.__guess = message.content

    #------------------COMMANDS------------------------

    
# !buzzer
  # Starts buzzer
  @commands.command(name = 'buzzer', description = 'Starts buzzer')
  async def buzzer(self, ctx, *, args: str):
      






# # !buzzer
#   # Starts buzzer
#   @commands.command(name = 'buzzer', description = 'Starts buzzer')
#   async def buzzer(self, ctx, *, args: str):
#     #   await self.bot.wait_for('message', timeout = 15)


    


    def setup(bot):
        bot.add_cog(Jeopardy(bot))