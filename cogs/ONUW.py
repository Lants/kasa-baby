# One Night Ultimate Werewolf
# 3+ players

from discord.ext import commands
import random

ALIVE = 1
DEAD = 0



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
        def __init__(self):
            self.__playing = False
            self.__n = 0
            self.__playerList = []
            self.__roleList = []

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
            print(n)

        async def setPlayers(self, ctx, mentionList, roleAlive):
            # print(mentionList)
            i = 0
            for member in mentionList:
                self.__playerList.append(Onuw.Player(member, None, ALIVE))
                await ctx.send(self.__playerList)
                # Assign custom role (get guild's role by id, then add to member)
                # await member.add_roles(ctx.guild.get_role(roleAlive))
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
                self.__roleList = [1, 2, 3, 4, 5, 7]
            elif n == 4:
                self.__roleList = [1, 2, 3, 4, 5, 7, 10]
            elif n == 5:
                self.__roleList =  [1, 2, 3, 4, 5, 7, 10, 0]
            elif n == 6:
                self.__roleList = [1, 2, 3, 4, 5, 7, 8, 10, 0]
            elif n == 7:
                self.__roleList = [1, 2, 3, 4, 5, 7, 8, 10, 6, 0]
            elif n == 8:
                self.__roleList = [1, 2, 3, 4, 5, 9, 7, 8, 10, 1, 9]
            elif n == 9:
                self.__roleList = [1, 2, 3, 4, 5, 9, 7, 8, 1, 0, 10, 9]
            elif n == 10:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0]
            elif n == 11:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 0]
            elif n == 13:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 7]
            elif n == 14:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 7, 2]
            elif n == 15:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 7, 2, 9]
            elif n == 16:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 7, 2, 1, 3]

            rolesTemp = self.__roleList.copy()
            random.shuffle(rolesTemp)
            print(rolesTemp)
            print(self.__roleList)
            for user in self.__playerList:
                user.__role = rolesTemp.pop()
                print(user.__role + " " + rolesTemp)
            
        # Print roles
        async def printRoles(self, ctx):
            rolePrinted = []
            for role in self.__roleList:
                rolePrinted.append(self.__RoleSwitcher.get(role))
            await ctx.send(rolePrinted)


        # Game functions
        async def setupGame(self, ctx, onuwInstance):
            await onuwInstance.sortRoles()
            await onuwInstance.printRoles(ctx)



    #------------------COMMANDS------------------------

    # !onuw
    # Starts an instance of One Night Ultimate Werewolf in current context
    @commands.command(name = "ONUW", description = "Play One Night Ultimate Werewolf!\nUsage: !ONUW <n> <user1> <user2> <user3>...\nwhere n is the number of players and <user#> is a player")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuw(self, ctx, *args):
        await ctx.send("Starting One Night Ultimate Werewolf >:)")

        mentionList = ctx.message.mentions
        onuwInstance = self.OnuwGame()

        roleIDList = await self.onuwRoles(ctx)
        await onuwInstance.setPlayers(ctx, mentionList, roleIDList[0])
        await onuwInstance.setupGame(ctx, onuwInstance)

    # !onuwRoles
    # Creates necessary roles for ONUW game
    @commands.command(name = "OnuwRoles", description = "Only use this once per server. Creates necessary roles for ONUW game\nUsage: !OnuwRoles")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuwRoles(self, ctx):
        createAlive, createDead = True, True
        onuwRoleIDList = [0, 0]
        roleList = await ctx.guild.fetch_roles()
        for role in roleList:
            print(role.name)
            if role.name == "ONUW Alive":
                createAlive = False
                onuwRoleIDList[0] = role.id
            if role.name == "ONUW Dead":
                createDead = False
                onuwRoleIDList[1] = role.id
        if createAlive:
            onuwRoleIDList[0] = (await ctx.guild.create_role(name = "ONUW Alive", mentionable = True)).id
        if createDead:
            onuwRoleIDList[1] = (await ctx.guild.create_role(name = "ONUW Dead", mentionable = True)).id
        if createAlive and createDead:
            await ctx.send("ONUW roles created!")
        else:
            await ctx.send("ONUW roles updated!")

        return onuwRoleIDList
      







    


def setup(bot):
    bot.add_cog(Onuw(bot))