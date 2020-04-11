import discord

client = discord.Client()

channelID = 0
messageID = 0
lance = 187028470998499340
currentPurger = 0

def is_admin(m):
    return 'Admin' == m.author.top_role.name or m.author.id == lance

def is_author(m):
    print('comparing ' + str(m.author.id) + ' to ' + str(currentPurger))
    return m.author.id == currentPurger

async def purgeAdmin(n, chan, targetOption, mentions):
    try:
        n = int(n) + 1
        if n > 70:
            n = 70
        if targetOption == 'all':
            await discord.TextChannel.purge(chan, limit = n, check = is_author)
        else:
            # for targetUser in mentions:
            return
    except:
        chan.send("아빠, that doesn't make any sense! <!purgeAdmin target-user #>")
        
async def purge(n, chan):
    # try:
        n = int(n) + 1
        if n > 7:
            n = 70
        print(currentPurger)
        await discord.TextChannel.purge(chan, limit = n, check = is_author)
    # except:
        # await chan.send("오빠/누나, that's not a number! <!purge #lines>")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




@client.event
async def on_message(message):

    

    if message.author == client.user:
        return

    channelID = message.channel.id
    messageID = message.id

    print("message: " + message.content)

    if message.content.startswith('!'):
        inputContent = str(message.content[1:])
        print('Message: ' + inputContent + " | ID: " + str(message.id))

        if inputContent == 'help':
            print('received help')
            await message.channel.send("""I'm the kasa baby uwu
            !help - this screen
            !close() - put me to bed! only parents though :) (Admin only)
            more here later :D""")
        
        if inputContent.startswith('hello'):
            print('received hello')
            await message.channel.send('Hello!')

        if inputContent == 'close()':
            await message.delete()
            if is_admin(message):
                await message.channel.send("nighty night! I go sleep now @" + str(message.author.display_name))
                await client.close()

        ###---PURGE---###
        inputArray = []
        if inputContent.lower().lstrip().rstrip().startswith('purgeadmin '):
            if is_admin(message):
                inputArray = inputContent.split()
                if len(inputArray) >= 3 and str(inputArray[2]) == 'all':
                    purgeAdmin(inputArray[1], message.channel, 'all', message.mentions)
                elif len(inputArray) == 3:
                    purgeAdmin(inputArray[1], message.channel, 'mention', message.mentions)
                else:
                    message.channel.delete()
                    message.channel.send("""아빠, use the command correctly!
                    <!purgeAdmin #lines all>
                    <!purgeAdmin #lines @user1 @user2...>""")
            else:
                message.channel.send("u mean <!purge #>? only 부모님 can use purgeAdmin!")
                await message.delete()

        if inputContent.lower().lstrip().rstrip().startswith('purge '):
            inputArray = inputContent.split()
            currentPurger = message.author.id
            print(currentPurger)
            await purge(inputArray[1], message.channel)
        

client.run('Njk4MjU3NjQ5MzA4OTI1OTky.XpDOEQ.JZUlYE_fa_C0g9fQGoqN4ls9YEE')