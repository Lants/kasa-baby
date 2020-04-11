import discord

client = discord.Client()

lance = 187028470998499340
print("INIT VARS")

def is_admin(m):
    return 'Admin' == m.author.top_role.name or m.author.id == lance

def is_author(m, currPurger):
    return m.author.id == currPurger

async def purgeAdmin(n, chan, targetOption, mentions):
    try:
        n = int(n) + 1
        if n > 70:
            n = 70
        if targetOption == 'all':
            await discord.TextChannel.purge(chan, limit = n)
        else:
            async for m in chan.history(limit = n):
                for targetUser in mentions:
                    if is_author(m, m.id):
                        await m.delete()
    except:
        chan.send("아빠, that doesn't make any sense! <!purgeAdmin target-user #>")
        
async def purge(n, chan, currPurger):
    try:
        n = int(n) + 1
        if n > 7:
            n = 70
        async for m in chan.history(limit = n):
            if is_author(m, currPurger):
                await m.delete()
    except:
        await chan.send("오빠/누나, that's not a number! <!purge #lines>")

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
                    await purgeAdmin(inputArray[1], message.channel, 'all', message.mentions)
                elif len(inputArray) >= 3:
                    await purgeAdmin(inputArray[1], message.channel, 'mention', message.mentions)
                else:
                    await message.channel.delete()
                    await message.channel.send("""아빠, use the command correctly!
                    <!purgeAdmin #lines all>
                    <!purgeAdmin #lines @user1 @user2...>""")
            else:
                await message.channel.send("u mean <!purge #>? only 부모님 can use purgeAdmin!")

        if inputContent.lower().lstrip().rstrip().startswith('purge '):
            inputArray = inputContent.split()
            currentPurger = message.author.id
            print(currentPurger)
            await purge(inputArray[1], message.channel, currentPurger)
        

client.run('Njk4MjU3NjQ5MzA4OTI1OTky.XpIoNA.Rz0ICCsO9sujh-9j7gojef63G-Y')