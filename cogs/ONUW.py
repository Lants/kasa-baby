# One Night Ultimate Werewolf
# 3+ players

import discord
from discord.ext import commands
import random, asyncio

ALIVE = 0
DEAD = 1
AWAKE = 2
SECRET = 3
NARRATOR = 4




class Onuw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # ---Player inner class---
    class Player(object):
        def __init__(self, user, role, status):
            self.__user = user
            self.__role = role
            self.__status = status
        
        def getUser(self):
            return self.__user
        def getRole(self):
            return self.__role
        async def setRole(self, role: int):
            self.__role = role
        def getStatus(self):
            return self.__status
        async def setStatus(self, status: int):
            self.__status = status

    # ---ONUW game inner class---
    class OnuwGame(object):
        def __init__(self, IDList):
            self.__playing = False
            self.__n = 0
            self.__playerList = []
            self.__roleList = []
            self.__tableCards = []
            self.__IDList = IDList

            self.__RoleSwitcher = {
                0: "VILLAGER",
                1: "WEREWOLF",
                2: "MINION",
                3: "SEER",
                4: "ROBBER",
                5: "TROUBLEMAKER",
                6: "TANNER",
                7: "DRUNK",
                8: "HUNTER",
                9: "MASON",
                10: "INSOMNIAC"}

        # Getters and Setters
        async def setN(self, n):
            self.__n = n
            print("\n\n\n\n\nNumber of players:" + str(n))

        async def setPlayers(self, ctx, mentionList):
            i = 0
            for member in mentionList:
                self.__playerList.append(Onuw.Player(member, None, ALIVE))
                # Assign custom role (get guild's role by id, then add to member)
                await member.add_roles(ctx.guild.get_role(self.__IDList[ALIVE]))
                await member.remove_roles(ctx.guild.get_role(self.__IDList[DEAD]))
                i += 1
            await self.setN(i)


        async def setPlaying(self, status: bool):
            self.__playing = status

        def getN(self):
            return self.__n

        def getPlayers(self):
            return self.__playerList
        
        def isPlaying(self):
            return self.__playing

        # Sort Roles
        async def sortRoles(self):
            n = self.getN()
            cardCount = n + 3
            
            if n == 3:
                self.__roleList = [1, 1, 3, 4, 5, 7]
            elif n == 4:
                self.__roleList = [1, 1, 3, 4, 5, 7, 10]
            elif n == 5:
                self.__roleList =  [1, 1, 3, 4, 5, 7, 10, 0]
            elif n == 6:
                self.__roleList = [1, 2, 3, 4, 5, 7, 0, 10, 0]
            elif n == 7:
                self.__roleList = [1, 1, 3, 4, 5, 7, 8, 10, 0, 0]
            elif n == 8:
                self.__roleList = [1, 1, 3, 4, 5, 9, 7, 8, 10, 2, 9]
            elif n == 9:
                self.__roleList = [1, 1, 3, 4, 5, 9, 7, 8, 1, 2, 10, 9]
            elif n == 10:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0]
            elif n == 11:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 0]
            elif n == 13:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 7]
            elif n == 14:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 7, 2]
            elif n == 15:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 7, 2, 9]
            elif n == 16:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 1, 2, 1, 3]

            self.__tableCards = self.__roleList.copy()
            random.shuffle(self.__tableCards)
            for user in self.__playerList:
                await user.setRole(self.__tableCards.pop())
                print("\n%s is assigned to %s" % (user.getUser().name, user.getRole()))

            print("Available cards:")
            print(self.__roleList)
            print("Cards left on table:")
            print(self.__tableCards)
            
        # Print roles
        async def printRoles(self, ctx):
            rolePrinted = []
            for role in self.__roleList:
                rolePrinted.append(self.__RoleSwitcher.get(role))
            await ctx.send(rolePrinted)


        # Game functions
        async def setupGame(self, ctx):
            await self.sortRoles()
            await self.startGame(ctx)

        async def startGame(self, ctx):
            # DM each player their initial card.
            for player in self.__playerList:
                if player.getUser().name == "Lancer":
                    print("Found Lancer! Attempting to PM role...")
                    await player.getUser().send("You are a(n) %s" % self.__RoleSwitcher.get(player.getRole()))

            # Night Phase ---------

            def checkReaction(reaction, user):
                return reaction.emoji == "👍"

            narrator = ctx.guild.get_channel(self.__IDList[NARRATOR])
            secret = ctx.guild.get_channel(self.__IDList[SECRET])

            await narrator.send("Check your PMs for your assigned role! Have one person 'Thumbs Up' react to start One Night Ultimate Werewolf >:)")

            await ctx.bot.wait_for("reaction_add", timeout = 120, check = checkReaction)

            await narrator.send("Dusk approaches, everyone go to sleep...")
            await asyncio.sleep(5)
            await narrator.send("Werewolves are awakened by the rising moon")



    #------------------COMMANDS------------------------

    # !onuw
    # Starts an instance of One Night Ultimate Werewolf in current context
    @commands.command(name = "ONUW", description = "Play One Night Ultimate Werewolf!\nUsage: !ONUW <n> <user1> <user2> <user3>...\nwhere n is the number of players and <user#> is a player")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuw(self, ctx, *args):
        
        mentionList = ctx.message.mentions
        
        IDList = await self.onuwChannel(ctx)
        onuwInstance = self.OnuwGame(IDList)

        await onuwInstance.setPlayers(ctx, mentionList)
        await onuwInstance.setupGame(ctx)


    # !onuwRoles
    # Creates necessary roles for ONUW game
    @commands.command(name = "OnuwRoles", description = "DO NOT USE UNLESS YOU KNOW WHAT YOU'RE DOING. Creates necessary roles for ONUW game\nUsage: !OnuwRoles")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuwRoles(self, ctx):
        createAlive, createDead, createAwake = True, True, True
        onuwRoleIDList = [0, 0, 0]
        roleList = await ctx.guild.fetch_roles()
        for role in roleList:
            if role.name == "ONUW Alive":
                createAlive = False
                onuwRoleIDList[0] = role.id
            if role.name == "ONUW Dead":
                createDead = False
                onuwRoleIDList[1] = role.id
            if role.name == "ONUW Awake":
                createAwake = False
                onuwRoleIDList[2] = role.id
        if createAlive:
            onuwRoleIDList[ALIVE] = (await ctx.guild.create_role(name = "ONUW Alive", mentionable = True)).id
        if createDead:
            onuwRoleIDList[DEAD] = (await ctx.guild.create_role(name = "ONUW Dead", mentionable = True)).id
        if createAwake:
            onuwRoleIDList[AWAKE] = (await ctx.guild.create_role(name = "ONUW Awake", mentionable = True)).id
        if createAlive and createDead and createAwake:
            await ctx.send("ONUW roles created!")
        else:
            await ctx.send("ONUW roles updated!")

        return onuwRoleIDList

    # !OnuwChannel
    # Creates channel made by ONUW game
    @commands.command(name = "OnuwChannel", description = "DO NOT USE UNLESS YOU KNOW WHAT YOU'RE DOING. Creates secret channel for ONUW game.\nUsage: !OnuwChannel")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuwChannel(self, ctx):
        createChannel, createNarrator = True, True
        for chan in ctx.guild.channels:
            if "onuw-secret" == chan.name:
                createChannel = False
                IDSecret = chan.id
            if "onuw-narrator" == chan.name:
                createNarrator = False
                IDNarrator = chan.id

        onuwRoleIDList = await self.onuwRoles(ctx)

        overwritesSecret = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.guild.get_role(onuwRoleIDList[AWAKE]): discord.PermissionOverwrite(read_messages = True)
        }

        overwritesNarrator = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages = False)
        }

        if createChannel:
            IDSecret = (await ctx.guild.create_text_channel(name = "onuw-secret", overwrites = overwritesSecret)).id
        if createNarrator:
            IDNarrator = (await ctx.guild.create_text_channel(name = "onuw-narrator", overwrites = overwritesNarrator)).id

        # 0) "Onuw Alive" ID. 1) "Onuw Dead" ID. 2) "Onuw Awake" ID. 3) "onuw-secret" channel ID. 4) "onuw-narrator" channel ID.
        onuwIDList = onuwRoleIDList
        onuwIDList.append(IDSecret)
        onuwIDList.append(IDNarrator)
        return onuwIDList
      







    


def setup(bot):
    bot.add_cog(Onuw(bot))