# One Night Ultimate Werewolf
# 3+ players

import discord
from discord.ext import commands
import random, asyncio, copy

BABYBOT = 698257649308925992

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
            self.__originalRole = role
        
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
            self.__tempCounter = 0

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

        def getTempCounter(self):
            return self.__tempCounter
        
        async def setTempCounter(self, n):
            self.__tempCounter = n

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
                self.__roleList = [1, 2, 3, 4, 5, 7]
            elif n == 4:
                self.__roleList = [1, 2, 3, 4, 5, 7, 10]
            elif n == 5:
                self.__roleList =  [1, 2, 3, 4, 5, 7, 10, 0]
            elif n == 6:
                self.__roleList = [1, 2, 3, 4, 5, 7, 9, 10, 9]
            elif n == 7:
                self.__roleList = [1, 2, 3, 4, 5, 7, 8, 10, 0, 0]
            elif n == 8:
                self.__roleList = [1, 1, 3, 4, 5, 9, 7, 8, 10, 2, 9]
            elif n == 9:
                self.__roleList = [1, 1, 3, 4, 5, 9, 7, 8, 0, 2, 10, 9]
            elif n == 10:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0]
            elif n == 11:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 0, 0]
            elif n == 13:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 0]
            elif n == 14:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 0, 0]
            elif n == 15:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 2, 0, 0]
            elif n == 16:
                self.__roleList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 1, 1, 2, 0, 0, 0]

            self.__tableCards = self.__roleList.copy()
            i = random.randrange(n) + 1
            while i > 0:
                random.shuffle(self.__tableCards)
                i -= 1
            tempCard = None
            for user in self.__playerList:
                tempCard = self.__tableCards.pop()
                ######################################## CHANGE THIS, DEVELOPMENTAL #######################################
                # Also edit "wake" function
                # if user.getUser().name == "Lancer":
                #     tempCard = TROUBLEMAKER
                # if user.getUser().name == "Peanut Colada":
                #     tempCard = DRUNK
                # if user.getUser().name == "ChongK":
                #     tempCard = ROBBER
                ######################################## ########################## #######################################
                await user.setRole(tempCard)
                self.__cardArray[tempCard].append(user)
                print("\n%s is assigned to %s" % (user.getUser().name, self.__RoleSwitcher.get(user.getRole())))

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
        
        async def getPlayerCards(self):
            cards = []
            for player in self.__playerList:
                cards.append("[%s, %s] " % (player.getUser().name, self.__RoleSwitcher.get(player.getRole())))
            return cards


        # Game functions
        async def setupGame(self, ctx):
            await self.sortRoles()
            await self.startGame(ctx)


        # Add ONUW Awake role to players with given card, then mention them
        async def wake(self, ctx, card):
            print("WAKE: %s" % self.__cardArray)
            for player in self.__cardArray[card]:
                await player.getUser().add_roles(ctx.guild.get_role(self.__IDList[AWAKE]))
                await ctx.guild.get_channel(self.__IDList[SECRET]).send(player.getUser().mention)

        # Remove ONUW Awake role to players with given card
        async def unwake(self, ctx, card):
            for player in self.__cardArray[card]:
                await player.getUser().remove_roles(ctx.guild.get_role(self.__IDList[AWAKE]))
            await ctx.guild.get_channel(self.__IDList[SECRET]).send("Please head back to the onuw-narrator channel")
            await asyncio.sleep(5)
            await self.clearSecret(ctx, 100)

        # Clear secret channel
        async def clearSecret(self, ctx, n):
            msgs = []
            n = int(n)
            async for msg in ctx.guild.get_channel(self.__IDList[SECRET]).history(limit = None):
                msgs.append(msg)
            await ctx.guild.get_channel(self.__IDList[SECRET]).delete_messages(msgs)

        # Update card array to match Player object's "role" field
        # Lance if you run into problems with cards being mixed up, this is probably the reason LOL
        async def updateCardArray(self, ctx):
            i = 0
            for cardRole in self.__cardArray:
                j = 0
                print("i: %d" % i)
                for player in cardRole:
                    print("i: %d, j: %d" % (i, j))
                    if player.getRole() != i:
                        self.__cardArray[player.getRole()].append(cardRole.pop(j))
                    j += 1
                i += 1

        async def startGame(self, ctx):
            # DM each player their initial card.
            for player in self.__playerList:
                    await player.getUser().send("Your card is: %s" % self.__RoleSwitcher.get(player.getRole()))

            # Night Phase ---------#############################################################

            def checkReactionStartGame(reaction, user):
                return reaction.emoji == "\U0001F43A" and reaction.message.channel.id == self.__IDList[NARRATOR] and reaction.count > len(self.__playerList)

            narrator = ctx.guild.get_channel(self.__IDList[NARRATOR])
            secret = ctx.guild.get_channel(self.__IDList[SECRET])

            msg = await narrator.send("Check your PMs for your assigned role! If you're assigned a role that has special tasks, a secret text channel will appear when necessary. You'll have a minute to do your actions, so take your time. \n```Click the wolf emoji to start One Night Ultimate Werewolf >:)```\n")
            await msg.add_reaction("\U0001F43A")
            await narrator.send("\n\nFor %d players, here are this round's available cards:\n" % self.getN())
            await self.printRoles(narrator)
            await ctx.bot.wait_for("reaction_add", timeout = 500, check = checkReactionStartGame)

            await narrator.send("``` ```\nDusk approaches, everyone go to sleep...:sunrise:")
            await asyncio.sleep(3)
            await narrator.send(":sleeping:")
            await asyncio.sleep(1)
            await narrator.send(":sleeping:")
            await asyncio.sleep(1)
            await narrator.send(":sleeping:")
            await asyncio.sleep(1)

            # Add Werewolves to secret channel with AWAKE role, then mention them
            await self.wake(ctx, WEREWOLF)

            await narrator.send("``` ```\n:full_moon: Werewolves are awakened by the rising moon :full_moon:\nYou must work together to fool the villagers. Meet your partner(s) in crime in the secret location.")
            
            # Simple check for werewolf reaction
            def checkReactionWerewolfSolo(reaction, user):
                return user.id == self.__cardArray[WEREWOLF][0].getUser().id and (reaction.emoji == "1️⃣" or reaction.emoji == "2️⃣" or reaction.emoji == "3️⃣") and reaction.message.channel.id == self.__IDList[SECRET]

            def checkReactionWerewolves(reaction, user):
                return reaction.count > len(self.__cardArray[WEREWOLF]) and reaction.message.channel.id == self.__IDList[SECRET]

            await narrator.send("You have 60 seconds before the Seer wakes up.")

            # Check if only 1 Werewolf
            if len(self.__cardArray[WEREWOLF]) == 1:
                msg = await secret.send("It's quite lonely here... Perhaps your comrades have fallen ill. You have enough time to reveal ONE of the 3 mystery (non-player) cards:")
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
                await msg.add_reaction("3️⃣")
                # Wait for a reaction, then reveal their chosen card
                try:
                    reac = await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionWerewolfSolo)
                    if reac[0].emoji == "1️⃣":
                        await secret.send("Card 1 is: %s" % self.__RoleSwitcher.get(self.__tableCards[0]))
                    elif reac[0].emoji == "2️⃣":
                        await secret.send("Card 2 is: %s" % self.__RoleSwitcher.get(self.__tableCards[1]))
                    elif reac[0].emoji == "3️⃣":
                        await secret.send("Card 3 is: %s" % self.__RoleSwitcher.get(self.__tableCards[2]))
                except:
                    print("Werewolf timed out")
                
            # Check if no Werewolves

            elif len(self.__cardArray[WEREWOLF]) == 0:
                await asyncio.sleep(random.randrange(15) + 12)
            else:
                msg = await secret.send("The Werewolves now know each others' scents. You must prevent each other from being lynched by the village. Click the wolf when you're ready to go back to bed.")
                await msg.add_reaction("\U0001F43A")
                try:
                    reac = await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionWerewolves)
                except:
                    print("Werewolves timed out")
            
            # SEER PHASE

            def checkReactionSeer(reaction, user):
                return reaction.message.channel.id == self.__IDList[SECRET] and user.id != BABYBOT
            await self.unwake(ctx, WEREWOLF)
            # Clear messages from secret channel
            await self.clearSecret(ctx, 100)
            
            await narrator.send("``` ```\nThe Werewolves have gone back to sleep. However, a Seer feels disturbed and wakes up. They decide to do a quick 60-second :crystal_ball: reading before going back to bed.\n")
            await narrator.send("Seers can either view 1 player's card or view 2 of the non-player cards.")
            
            await self.wake(ctx, SEER)

            if len(self.__cardArray[SEER]) > 0:
                await secret.send("As a Seer, you may either reveal the card of 1 slumbering villager, or 2 of the 3 mystery (non-player) cards.\n")
                await secret.send("```React to 1, 2, or 3 to select the card you wish to NOT see.```OR")
                msg = await secret.send("```Click the :crystal_ball: below the villager you wish to read```")
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
                await msg.add_reaction("3️⃣")
                await asyncio.sleep(1)

                for player in self.getPlayers(): # List out all players to secret channel, each with a :crystal_ball:
                    if (player not in self.__cardArray[SEER]):
                        msg = await ctx.guild.get_channel(self.__IDList[SECRET]).send(player.getUser().name)
                        await msg.add_reaction("🔮")
                
                reac = (await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionSeer))[0]

                try:
                    if reac.emoji == "1️⃣":
                        await secret.send("Card 2 & 3 are: %s, %s" % (self.__RoleSwitcher.get(self.__tableCards[1]), self.__RoleSwitcher.get(self.__tableCards[2])))
                    elif reac.emoji == "2️⃣":
                        await secret.send("Card 1 & 3 are: %s, %s" % (self.__RoleSwitcher.get(self.__tableCards[0]), self.__RoleSwitcher.get(self.__tableCards[2])))
                    elif reac.emoji == "3️⃣":
                        await secret.send("Card 2 & 3 are: %s, %s" % (self.__RoleSwitcher.get(self.__tableCards[0]), self.__RoleSwitcher.get(self.__tableCards[1])))
                    else:
                        for player in self.__playerList:
                            if reac.message.content == player.getUser().name:
                                await secret.send("%s's card is: %s" % (player.getUser().name, self.__RoleSwitcher.get(player.getRole())))
                except Exception as e:
                    print("Seer reaction error: %s" % e)
                
            else:
                await asyncio.sleep(random.randrange(18) + 8)

            await self.unwake(ctx, SEER)

            # MINION PHASE ---------------------------------
            if MINION in self.__roleList:
                await narrator.send("``` ```\nMinions, check your PMs to see the werewolves that you must assist")
                for player in self.__cardArray[MINION]:
                    if len(self.__cardArray[WEREWOLF]) == 0:
                        await player.getUser().send("``` ```There are no Werewolves this game! Try to frame a villager to win.")
                    else:
                        await player.getUser().send("``` ```Your Werewolves are:")
                        for werewolf in self.__cardArray[WEREWOLF]:
                            await player.getUser().send(werewolf.getUser().name)

                await asyncio.sleep(5)


            # MASON PHASE --------------------------
            if MASON in self.__roleList:
                await narrator.send("``` ```\nMasons, check your PMs to establish your psychic bond with the other Mason(s) in the game.")
                for player in self.__cardArray[MASON]:
                    if len(self.__cardArray[MASON]) == 1:
                        await player.getUser().send("``` ```You're the only Mason! You feel... empty...")
                    else:
                        await player.getUser().send("``` ```Masons:")
                        for mason in self.__cardArray[MASON]:
                            await player.getUser().send(mason.getUser().name)

                await asyncio.sleep(5)

            # ROBBER PHASE ------------------------ 

            def checkReactionSecret(reaction, user):
                return reaction.message.channel.id == self.__IDList[SECRET] and user.id != BABYBOT

            await narrator.send("``` ```\n...Do you hear that? It sounds like someone trying to be S N E A K Y!!! The Robber :knife: is awake ono :persevere:\n")
            await narrator.send("Robbers secretly trade their cards with another villager, effectively swapping teams. Only the Robber gets to see their new team. Robbers, you have 60 seconds")
            
            await self.wake(ctx, ROBBER)
            if len(self.__cardArray[ROBBER]) > 0:
                await secret.send("Robber, click the :knife: below the villager you'd like to swap cards with. Only teams will switch, not abilities.")
                for player in self.getPlayers(): # List out all players to secret channel, each with a :knife:
                    if (player not in self.__cardArray[ROBBER]):
                        msg = await ctx.guild.get_channel(self.__IDList[SECRET]).send(player.getUser().name)
                        await msg.add_reaction("🔪")
                    else:
                        robber = player

                try:
                    reac1 = (await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionSecret))[0]

                    for player in self.__playerList:
                        if reac1.message.content == player.getUser().name: # Swap cards (roles)
                            tempRobberRole = robber.getRole()
                            await robber.setRole(player.getRole())
                            await player.setRole(tempRobberRole)

                    await secret.send("Your new card is: %s" % self.__RoleSwitcher.get(robber.getRole()))
                    # print(self.__cardArray)
                    # await self.updateCardArray(ctx)
                    # print(self.__cardArray)
                except Exception as e:
                    print("Robber error: %s" % e)
            else:
                await asyncio.sleep(random.randrange(15) + 8)

            await self.unwake(ctx, ROBBER)
            
            # TROUBLEMAKER PHASE ------------------------------------
            
            await narrator.send("``` ```\nThe thief goes back to rest. In his place comes the Troublemaker, here to stir up trouble. The Troublemaker can swap any two villagers' cards, effectively swapping their teams.")
            await narrator.send("Troublemaker(s), you have 60 seconds to wreck havoc on the social ladder. Check the secret channel.")
            await self.wake(ctx, TROUBLEMAKER)

            if len(self.__cardArray[TROUBLEMAKER]) > 0:
                await secret.send("Troublemaker! Click the clowns :clown: below the 2 villagers you'd like to swap. Only their teams will switch, not their abilities.")
                await secret.send("```Due to Discord limitations, you cannot undo your first selection. Choose wisely.```\n")
                for player in self.getPlayers():
                    msg = await ctx.guild.get_channel(self.__IDList[SECRET]).send(player.getUser().name)
                    await msg.add_reaction("🤡")
            
                try:
                    reac1 = (await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionSecret))[0]
                    reac2 = copy.copy(reac1)
                    while reac1.message == reac2.message:
                        reac2 = (await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionSecret))[0]

                    for player in self.__playerList:
                        if reac1.message.content == player.getUser().name: # Swap cards (roles)
                            userSwap1 = player
                        if reac2.message.content == player.getUser().name:
                            userSwap2 = player
                    tempSwapRole = userSwap1.getRole()
                    await userSwap1.setRole(userSwap2.getRole())
                    await userSwap2.setRole(tempSwapRole)

                except Exception as e:
                    print("Troublemaker error: %s" % e)
            
            else:
                await asyncio.sleep(random.randrange(15) + 8)

            await self.unwake(ctx, TROUBLEMAKER)

            # DRUNK PHASE--------------------------------------------------
            await narrator.send("``` ```\nWhat's that ruckus? Oh, it's just the drunk :woozy_face: :beers:\nMans is so blacked out, he doesn't know his own card!")
            await narrator.send("Drunks secretly trade their card for any of the 3 non-player cards. The Drunk will assume the team of whichever card he gets, but he doesn't know what it is! 60 seconds, go!")
            
            await self.wake(ctx, DRUNK)
            if len(self.__cardArray[DRUNK]) > 0:
                msg = await secret.send("Hello, Drunk! Click the number of the mystery card you'd like to swap roles with. Only teams will switch, not abilities.")
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
                await msg.add_reaction("3️⃣")
                
                try:
                    reac = (await ctx.bot.wait_for("reaction_add", timeout = 60, check = checkReactionSecret))[0]
                    drunk = self.__cardArray[DRUNK][0].getRole()
                    if reac.emoji == "1️⃣":
                        await secret.send("Trading roles with card 1")
                        tempCard = self.__tableCards[0]
                        self.__tableCards[0] = drunk
                    elif reac.emoji == "2️⃣":
                        await secret.send("Trading roles with card 2")
                        tempCard = self.__tableCards[1]
                        self.__tableCards[1] = drunk
                    elif reac.emoji == "3️⃣":
                        await secret.send("Trading roles with card 3")
                        print("Card 3 is %d" %self.__tableCards[2])
                        tempCard = self.__tableCards[2]
                        self.__tableCards[2] = drunk

                    await self.__cardArray[DRUNK][0].setRole(tempCard)                    
                    
                except Exception as e:
                    print("Drunk error: %s" % e)
            else:
                await asyncio.sleep(random.randrange(15) + 8)

            print(await self.getPlayerCards())
            print(self.__tableCards)

            await self.unwake(ctx, DRUNK)

            # Insomniac phase-----------------------------------------------------
            if INSOMNIAC in self.__roleList:
                await narrator.send("``` ```\nInsomniacs, check your PMs to see your final card and team.")
                for player in self.__cardArray[INSOMNIAC]:
                    await player.getUser().send("``` ```Your role is: %s" % self.__RoleSwitcher.get(player.getRole()))
                await asyncio.sleep(5)

            await narrator.send("``` ```Now, discuss who to kill! If the tanner dies, it's his victory. If a Werewolf dies, the Villagers win. If a Villager dies and a Werewolf does NOT die, the Werewolves + Minions win. If the Hunter dies, he gets to take one person down with him.")

            await narrator.send("PM the bot a player name to vote against them. Here's the list of available roles again:\n\n")
            await self.printRoles(narrator)

            # def checkIsPlayerAndDM(msg):
            #     inPlayerList = False
            #     for player in self.__playerList:
            #         print("%s %s" % (player.getUser().name.lower(), msg.content.lower().strip()))
            #         if msg.content.lower().strip() == player.getUser().name.lower():
            #             inPlayerList = True
            #     return isinstance(msg.channel, discord.channel.DMChannel) and inPlayerList

            # # For every player, wait for a PM that contains an existing user's name.
            # voteList = []
            # msg = None
            # for player in self.__playerList:
            #     msg = await ctx.bot.wait_for('message', timeout = 5000, check = checkIsPlayerAndDM)
            #     voteList.append(msg)

            # voteList.sort()
            # await narrator.send("Votes: %s" % voteList)
            # await narrator.send("Actual Roles: %s" % await self.getPlayerCards())

            def checkIsCheckmark(reaction, user):
                return reaction.emoji == "✅"
            await ctx.bot.wait_for("reaction_add", timeout = 5000, check = checkIsCheckmark) # TODO: TEMPORARY PLEASE FIX AND MAKE BETTER
            await narrator.send(await self.getPlayerCards())

            
    ##########################################################################################################################################################
    ##################################################------------------COMMANDS------------------------######################################################
    ##########################################################################################################################################################

    # !onuw
    # Starts an instance of One Night Ultimate Werewolf in current context
    @commands.command(name = "ONUW", description = "Play One Night Ultimate Werewolf!\nUsage: !ONUW <n> <user1> <user2> <user3>...\nwhere n is the number of players and <user#> is a player")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuw(self, ctx, *args):
        await ctx.send("Welcome to One Night Ultimate Werewolf! It may take a second to set up, but please make your way over to the 'onuw-narrator' channel :)")

        mentionList = ctx.message.mentions
        
        IDList = await self.onuwChannel(ctx)
        onuwInstance = self.OnuwGame(IDList)
        print("\n\n\n\nCHANNELS AND ROLES SET UP, INSTANCE CREATED")
        await onuwInstance.setPlayers(ctx, mentionList)
        await onuwInstance.setupGame(ctx)


    # !onuwRoles
    # Creates necessary roles for ONUW game
    @commands.command(name = "OnuwRoles", description = "DO NOT USE UNLESS YOU KNOW WHAT YOU'RE DOING. Creates necessary roles for ONUW game\nUsage: !OnuwRoles")
    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    async def onuwRoles(self, ctx):
        print("Running ONUWRoles")
        onuwRoleIDList = [0, 0, 0]
        roleList = await ctx.guild.fetch_roles()
        print("Fetched roles")
        for role in roleList:
            print(role)
            if role.name == "ONUW Alive" or role.name == "ONUW Dead" or role.name == "ONUW Awake":
                await role.delete()

        # createAlive
        print("Creating Alive")
        onuwRoleIDList[ALIVE] = (await ctx.guild.create_role(name = "ONUW Alive", mentionable = True)).id
        print("Created Alive")
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
        print("Running ONUWChannel")
        for chan in ctx.guild.channels:
            if "onuw-secret" == chan.name or "onuw-narrator" == chan.name or "onuw-dead" == chan.name:
                await chan.delete()

        onuwRoleIDList = await self.onuwRoles(ctx)
        print(onuwRoleIDList)

        overwritesSecret = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.guild.get_role(onuwRoleIDList[AWAKE]): discord.PermissionOverwrite(read_messages = True),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(send_messages = False)
        }

        overwritesNarrator = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.guild.get_role(onuwRoleIDList[ALIVE]): discord.PermissionOverwrite(read_messages = True),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(send_messages = False),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(add_reactions = False),
            ctx.guild.get_role(onuwRoleIDList[DEAD]): discord.PermissionOverwrite(read_messages = True),
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

    # !OnuwInstructions
    # Prints out instructions for ONUW
    @commands.command(name = "ONUWInstructions", description = "Prints out instructions for One Night Ultimate Werewolf.")
    async def onuwInstructions(self, ctx):
        desc = """How to play One Night Ultimate Werewolf:

        Mostly, just follow the instructions of the narrator when you run !ONUW. Here's the basic concept: Every villager gets a "card", which is just a role.
        Some cards have special abilities. There will be 3 additional "mystery cards" added to the pile which aren't assigned to any villagers, but can be interacted with
        depending on your card (See bottom)

        Some players will be assigned to be "Werewolves," "Minions," or "Tanners." These cards are considered to be on a separate team
        from the villagers:
        Minions and Werewolves versus the Villagers, with the Tanners on their own team (their goal is to be lynched by the village, because they hate life).

        After being assigned cards, everyone goes to sleep. Villagers/Werewolves with special cards get to wake up one at a time to use their abilities. After all the
        special villagers wake up and do their tasks, everyone wakes up.

        At this point, everyone starts discussing to choose one person to lynch.
        If a Tanner is lynched, he wins.
        If any innocent Villager dies and a Werewolf does not also die, the Werewolves and Minions win.
        If any Werewolf dies, the Villagers win."""


        villager = "No special powers, just pay attention to what other villagers are saying and try to find the Werewolves."
        
        werewolf = "Your goal is to NOT be lynched by the village. Come up with clever ways to shift blame onto other Villagers. It's helpful to claim to be a different Villager! Common false identities include Villager, Drunk, Insomniac, and Mason."
        
        minion = "On the Werewolf team, but the Werewolves don't know it. Help your team by covering for your Werewolves or trying to make yourself look guilty. Dying does NOT mean your team loses."
        
        seer = "The Seer views any Villager's card. Alternatively, they can view any TWO of the mystery cards."

        robber = "Trades their own card for any other Villager's card, then views that card. Abilities do not get swapped, but teams do."

        troublemaker = "Secretly swaps any two Villagers' cards."

        tanner = "No special powers, but you win if you get lynched cuz ur a depresso espresso D:"

        drunk = "You glug glug til you black out, so you don't know your card. This is achieved by trading your \"Drunk\" card for any of the mystery cards."

        hunter = "If you are chosen to be lynched, you can choose one other villager to be killed with you. That is to say, if you die, you have a second chance to try to kill a Werewolf."

        mason = "There will be at least 2 Masons in the game. If more than 1 Mason is assigned to a player, all Masons will know the other Masons."

        insomniac = "At the end of the night, the Insomniac gets to view their final role in case it was shifted around."

        

        embed = discord.Embed(color=0x00ff00)
        embed.title = ("One Night Ultimate Werewolf Instructions")
        embed.description = desc
        embed.add_field(name = "Villager", value = villager)
        embed.add_field(name = "Werewolf", value = werewolf)
        embed.add_field(name = "Minion", value = minion)
        embed.add_field(name = "Seer", value = seer)
        embed.add_field(name = "Robber", value = robber)
        embed.add_field(name = "Troublemaker", value = troublemaker)
        embed.add_field(name = "Tanner", value = tanner)
        embed.add_field(name = "Drunk", value = drunk)
        embed.add_field(name = "Hunter", value = hunter)
        embed.add_field(name = "Mason", value = mason)
        embed.add_field(name = "Insomniac", value = insomniac)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Onuw(bot))