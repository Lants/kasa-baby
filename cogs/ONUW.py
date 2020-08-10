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
SPECTATE = 5

VILLAGER, WEREWOLF, MINION, SEER, ROBBER, TROUBLEMAKER, TANNER, DRUNK, HUNTER, MASON, INSOMNIAC = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10



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
            self.__cardArray = [[], [], [], [], [], [], [], [], [], [], []]

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
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 1, 2, 1, 0]

            self.__tableCards = self.__roleList.copy()
            i = random.randrange(n) + 1
            while i > 0:
                random.shuffle(self.__tableCards)
                i -= 1
            tempCard = None
            for user in self.__playerList:
                tempCard = self.__tableCards.pop()
                await user.setRole(tempCard)
                self.__cardArray[tempCard].append(user)
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


        # Add ONUW Awake role to players with given card, then mention them
        async def wake(self, ctx, card):
            for player in self.__cardArray[card]:
                await player.getUser().add_roles(ctx.guild.get_role(self.__IDList[AWAKE]))
                await ctx.guild.get_channel(self.__IDList[SECRET]).send(player.getUser().mention)

        # Remove ONUW Awake role to players with given card
        async def unwake(self, ctx, card):
            for player in self.__cardArray[card]:
                await player.getUser().remove_roles(ctx.guild.get_role(self.__IDList[AWAKE]))
            await asyncio.sleep(5)

        # Clear secret channel
        async def clearSecret(self, ctx, n):
            msgs = []
            n = int(n)
            async for msg in ctx.guild.get_channel(self.__IDList[SECRET]).history(limit = None):
                msgs.append(msg)
            await ctx.guild.get_channel(self.__IDList[SECRET]).delete_messages(msgs)

        async def startGame(self, ctx):
            # DM each player their initial card.
            for player in self.__playerList:
                if player.getUser().name == "Lancer" or player.getUser().name == "Peanut Colada" or player.getUser().name == "AutoCarry":
                    print("Found Lancer! Attempting to PM role...")
                    await player.getUser().send("You are a(n) %s" % self.__RoleSwitcher.get(player.getRole()))

            # Night Phase ---------#############################################################

            def checkReactionStartGame(reaction, user):
                return reaction.emoji == "\U0001F43A"

            narrator = ctx.guild.get_channel(self.__IDList[NARRATOR])
            secret = ctx.guild.get_channel(self.__IDList[SECRET])

            msg = await narrator.send("Check your PMs for your assigned role! Have one person click the wolf emoji to start One Night Ultimate Werewolf >:)")
            await msg.add_reaction("\U0001F43A")
            await narrator.send("\n\nFor %d players, here are this round's available cards:\n" % self.getN())
            await self.printRoles(narrator)
            await ctx.bot.wait_for("reaction_add", timeout = 120, check = checkReactionStartGame)

            await narrator.send("``` ```\nDusk approaches, everyone go to sleep...:sunrise:")
            await asyncio.sleep(3)
            await narrator.send(":sleeping:")
            await asyncio.sleep(1)
            await narrator.send(":sleeping:")
            await asyncio.sleep(1)
            await narrator.send(":sleeping:")
            await asyncio.sleep(2)

            # Add Werewolves to secret channel with AWAKE role, then mention them
            await self.wake(ctx, WEREWOLF)

            await narrator.send("``` ```\n:full_moon: Werewolves are awakened by the rising moon :full_moon:\nYou must work together to fool the villagers. Meet your partner(s) in crime in the secret location.")
            
            # Simple check for werewolf reaction
            def checkReactionWerewolfSolo(reaction, user):
                return user.id == self.__cardArray[WEREWOLF][0].getUser().id and (reaction.emoji == "1️⃣" or reaction.emoji == "2️⃣" or reaction.emoji == "3️⃣")

            def checkReactionWerewolves(reaction, user):
                return user.role == self.IDList[AWAKE] and reaction.emoji == "\U0001F43A"

            await asyncio.sleep(3)
            await narrator.send("You have 30 seconds before the Seer wakes up.")

            # Check if only 1 Werewolf
            if len(self.__cardArray[WEREWOLF]) == 1:
                msg = await secret.send("It's quite lonely here... Perhaps your comrades have fallen ill. You have enough time to reveal ONE of the three mystery cards:")
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
                await msg.add_reaction("3️⃣")
                # Wait for a reaction, then reveal their chosen card
                try:
                    reac = await ctx.bot.wait_for("reaction_add", timeout = 30, check = checkReactionWerewolfSolo)
                except:
                    print("Werewolf timed out")
                if reac[0].emoji == "1️⃣":
                    await secret.send("Card 1 is: %s" % self.__RoleSwitcher.get(self.__tableCards[0]))
                elif reac[0].emoji == "2️⃣":
                    await secret.send("Card 2 is: %s" % self.__RoleSwitcher.get(self.__tableCards[1]))
                elif reac[0].emoji == "3️⃣":
                    await secret.send("Card 3 is: %s" % self.__RoleSwitcher.get(self.__tableCards[2]))
            # Check if no Werewolves
            elif len(self.__cardArray[WEREWOLF]) == 0:
                asyncio.sleep(random.randrange(19) + 10)
            else:
                msg = await secret.send("The two Werewolves now know each others' scents. You must prevent each other from being lynched by the village. Click the wolf when you're ready to go back to bed.")
                await msg.add_reaction("\U0001F43A")
                try:
                    for player in self.__cardArray[WEREWOLF]:
                        reac = await ctx.bot.wait_for("reaction_add", timeout = 30, check = checkReactionWerewolves)
                except:
                    print("Werewolves timed out")
            
            # SEER PHASE

            def checkReactionSeer(reaction, user):
                return user.role == self.IDList[AWAKE] and (reaction.emoji == "1️⃣" or reaction.emoji == "2️⃣" or reaction.emoji == "3️⃣")
            def checkMentionSeer(msg):
                for mentions in msg.mentions:
                    if mention == self.__playerList.getUser():
                        return True
                return False
            await self.unwake(ctx, WEREWOLF)
            # Clear messages from secret channel
            await self.clearSecret(ctx, 100)
            
            await narrator.send("``` ```\nThe Werewolves have gone back to sleep. However, a Seer feels disturbed. They decide to do a quick 30-second :crystal_ball: reading before going back to bed.\n")
            
            await self.wake(ctx, SEER)

            await secret.send("As a Seer, you may either reveal the card of one slumbering villager, or two of the mystery cards.\n")
            await secret.send("Mention (@username) to reveal their role ```OR``` React to 1, 2, or 3 to select the card you wish to NOT see.")
            # try:
            #     pending_tasks = [ctx.bot.wait_for("reaction_add", timeout = 40, check = checkReactionSeer),
            #         ctx.bot.wait_for("message", timeout = 40, check = checkMentionSeer)]
            #     done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when = asyncio.FIRST_COMPLETED)
            #     for task in pending_tasks:
            #         task.cancel()
            # except:
            #     print("Seer thingy failed")



            

            


    #------------------COMMANDS------------------------

    # !onuw
    # Starts an instance of One Night Ultimate Werewolf in current context
    @commands.command(name = "ONUW", description = "Play One Night Ultimate Werewolf!\nUsage: !ONUW <n> <user1> <user2> <user3>...\nwhere n is the number of players and <user#> is a player")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuw(self, ctx, *args):
        await ctx.send("Welcome to One Night Ultimate Werewolf! It may take a second to set up, but please make your way over to the 'onuw-narrator' channel :)")

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
        onuwRoleIDList = [0, 0, 0]
        roleList = await ctx.guild.fetch_roles()
        for role in roleList:
            if role.name == "ONUW Alive" or role.name == "ONUW Dead" or role.name == "ONUW Awake":
                await role.delete()

        # createAlive
        onuwRoleIDList[ALIVE] = (await ctx.guild.create_role(name = "ONUW Alive", mentionable = True)).id
        # createDead
        onuwRoleIDList[DEAD] = (await ctx.guild.create_role(name = "ONUW Dead", mentionable = True)).id
        # createAwake
        onuwRoleIDList[AWAKE] = (await ctx.guild.create_role(name = "ONUW Awake", mentionable = True)).id

        return onuwRoleIDList

    # !OnuwChannel
    # Creates channel made by ONUW game
    @commands.command(name = "OnuwChannel", description = "DO NOT USE UNLESS YOU KNOW WHAT YOU'RE DOING. Creates secret channel for ONUW game.\nUsage: !OnuwChannel")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuwChannel(self, ctx):
        for chan in ctx.guild.channels:
            if "onuw-secret" == chan.name or "onuw-narrator" == chan.name or "onuw-dead" == chan.name:
                await chan.delete()

        onuwRoleIDList = await self.onuwRoles(ctx)

        overwritesSecret = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.guild.get_role(onuwRoleIDList[AWAKE]): discord.PermissionOverwrite(read_messages = True),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(send_messages = False)
        }

        overwritesNarrator = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.guild.get_role(onuwRoleIDList[ALIVE]): discord.PermissionOverwrite(read_messages = True),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(send_messages = False)
        }

        overwritesSpectate = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(read_messages = True)
        }

        IDSecret = (await ctx.guild.create_text_channel(name = "onuw-secret", overwrites = overwritesSecret, position = 2)).id
        IDNarrator = (await ctx.guild.create_text_channel(name = "onuw-narrator", overwrites = overwritesNarrator, position = 1)).id
        IDSpectate = (await ctx.guild.create_text_channel(name = "onuw-dead", overwrites = overwritesSpectate, position = 3)).id

        # 0) "Onuw Alive" ID. 1) "Onuw Dead" ID. 2) "Onuw Awake" ID. 3) "onuw-secret" channel ID. 4) "onuw-narrator" channel ID. 5) "onuw-dead" channel ID.
        onuwIDList = onuwRoleIDList
        onuwIDList.append(IDSecret)
        onuwIDList.append(IDNarrator)
        onuwIDList.append(IDSpectate)
        return onuwIDList
      







    


def setup(bot):
    bot.add_cog(Onuw(bot))