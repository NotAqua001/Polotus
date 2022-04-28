import os
os.system('pip3 install -r requirements.txt')

import discord
import datetime
from discord.utils import get
from discord_slash import SlashCommand
import json
from main1 import add_server, all_servers, get_amount, get_server, delete_server, get_warns,add_warn,add_amount, get_greet,add_greet,remove_greet,get_users,add_user,add_money,share_money, get_info,give_money,remove_money,add_inventory,update_greet, add_funcmd, get_funcmd, remove_funcmd, add_chatbot, get_chatbot, remove_chatbot, add_joinchannel, get_join_channels, remove_joinchannel
from giphy_client.rest import ApiException
import giphy_client
from discord.ext import commands, tasks
import asyncio
import random
from prsaw import RandomStuffV2
import DiscordUtils
import aiosqlite
import aiohttp
import youtube_dl
from async_timeout import timeout
import functools
import itertools
import math
import warnings

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(
    command_prefix='c!' , intents=intents, case_insensitve=True)
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)
rs = RandomStuffV2(async_mode=True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
client.session = aiohttp.ClientSession()

@client.event
async def on_member_join(member):
    with open("logs.txt", "a") as logsFile:
        logsFile.write("\n[{}] {} just joined the server".format(datetime.datetime.now(), member.name))
	
activity_string = '{} Servers.'.format(len(client.guilds))
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))
    print("Canopus#8817 Is Ready To Go!!!")
    await status_task()

async def status_task():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Your Commands'))
        await asyncio.sleep(5)
       
	
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user and message.content != "c!help":
        await message.channel.send('Type `c!help` for help.')

    users = get_funcmd()
    for i in users:
      if i[1] == message.author.id:
        await message.channel.send(f"{message.author.mention} shitt yourself")
    channels = get_chatbot();
    if client.user == message.author:
      return
    for i in channels:
      if message.channel.id == i[1]:
        try:
          if "@" not in message.content:
            response = await rs.get_ai_response(message.content)
            await message.reply(response)
        except:
          await message.reply("No answer, lol")
    if message.content.startswith(f"<@!{client.user.id}>") and len(message.content) == len(f"<@!{client.user.id}>"):
        await message.channel.send("My prefix is `c!`")
    await client.process_commands(message)

@client.command()
async def servers(ctx):
    activeservers = client.guilds
    sum = 0
    for guild in activeservers:
        print(f"name: {guild.name} | member count: {guild.member_count}, id = {guild.id}")
@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
    
client.sniped_messages = {}

@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)

@client.command(help="c!reactrole <emoji> <role> <description>")
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)


@client.command()
async def chatbot(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channels = get_chatbot()
        valid = False
        try:
            for i in channels:
                if i[1] == ctx.channel.id:
                    remove_chatbot(ctx.channel.id)
                    embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Disabled chatbot announcement on: {ctx.channel.mention}", color=0xFF0000)
                    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
                    await ctx.channel.send(embed=embed)
                    valid = True
                    break
        except:
            valid=False
        if valid == False:
            add_chatbot(ctx.channel.id)
            embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Enabled chatbot announcement on: {ctx.channel.mention}", color=0x00FF00)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
            await ctx.channel.send(embed=embed)
    else:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="<:1887crossbluepurple:927951094666113085>")
        await ctx.channel.send(embed=embed1)

@client.command()
async def funcmd(ctx, user : discord.Member):
  if ctx.author.id == 758697679667855433:
      add_funcmd(user.id)
      await ctx.channel.send("done")

@client.command()
async def delfuncmd(ctx, user : discord.Member):
  if ctx.author.id == 758697679667855433:
      remove_funcmd(user.id)
      await ctx.channel.send("done")


@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned: {user.mention}")

@unban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    try:
        channel = ctx.channel
        channel_position = channel.position
        
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.edit(position=channel_position, sync_permissions=True)
        embed = discord.Embed(description=f"**{ctx.author}** nuked this channel.", color=0x0000FF)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_image(url="https://media.giphy.com/media/nv6HcRbIv6IZa/giphy.gif")
        embed.set_footer(text=f"| Canopus Bot |   {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await new_channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |   {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@client.command()
async def help(ctx):
    embed = discord.Embed(title=" Canopus Bot  Help",description="""**My prefix:** `c!`
    
    📝 **Help Menu**
    `c!help`
    
   <:4323blurpleverifiedbotdeveloper:927951337013002311>   **Bot Info Menu**
    `c!botinfo` `c!web` `c!vote`
    
    <:3372xmasstaffshield:927951263142924330> **Moderation/Administration Menu**
    `c!warn` `c!hide` `c!nuke` `c!greet` `c!lock` `c!mute` `c!kick` `c!ban` `c!reactrole` `c!unmute`   `c!unhide` `c!unlock` `c!unban` `c!role` `c!unrole` `c!purge` `c!embed` `c!snipe` `c!timeout`

<:Premium:939606784241438810> **Premium Menu**
 `c!buy` `c!premium`

<a:2659tadapurple:927951128065368064> **Giveaway Menu**
`c!gstart` `c!gend` `c!greroll`

 <a:8223blobragequit:927951451014189056> **Fun Menu**  
    `c!whois` `c!8ball` `c!hack` `c!gif` `c!ping`  `c!meme` `c!serverinfo` `c!kill` `c!avatar` `c!banner` 

   <:6882blueliquidmoon:927951419322040400> **Economy Menu**
    `c!balance` `c!beg` `c!bet` `c!daily` `c!share` `c!bet` `c!shop`
     
  <:6380pixelsymbolplus:927951366008225852> **Invites Menu**
    `c!top` `c!invites` `c!restinvites all` `c!joinchannel` `c!removejoinchannel`

   <a:9220cdspin:927951481867472906> **Music Menu**
    `c!play` `c!queue` `c!now` `c!remove [number]` `c!loop` `c!skip` `c!volume` `c!disconnect` `c!shuffle` `c!summon` `c!join` `c!leave`
    
   <:Support:927951540432560168> [Get Support](https://discord.gg/NjX9XuMACb)

    <:6380pixelsymbolplus:927951366008225852> [Invite the bot here](https://discord.com/oauth2/authorize?client_id=924936306126106634&scope=bot%20applications.commands&permissions=8589934591)

                          <:4323blurpleverifiedbotdeveloper:927951337013002311>  Our Developers <a:6686arrowcyan:927951395280285736> `c!botinfo`""", color=0xfcfb04)
    embed.set_footer(text=f"Requested by {ctx.author} | Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}", icon_url=f"{ctx.author.avatar_url}")
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,user:discord.Member,*,reason="No reason provided"):
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Successfully kicked **{user}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| | Canopus Bot |  |{datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url=(f"{client.avatar.url}"))
        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Unable to kick member.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@kick.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,user:discord.Member,*,reason="No reason provided"):
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Successfully Banned **{user}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Unable to ban member.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@ban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Canopus Mute")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Canopus Mute")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    valid = False
    warns = get_warns()
    for i in warns:
        if i[1] == ctx.guild.id:
            valid = True
            break
        else:
            valid = False
    if valid == False:
        add_warn(ctx.guild.id)
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:** Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #1 Bot {datetime.datetime.now().hour}:{datetime.datetime.now().minute}", icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:2866zenitsuwtf:927951218733613086> `Case #1` {member.mention} has been muted.")
    else:

        add_amount(ctx.guild.id)
        amount = get_amount(ctx.guild.id)
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:** Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #{amount}•Bot{datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:2866zenitsuwtf:927951218733613086> `Case #{amount}` {member.mention} has been muted.")
    await member.add_roles(mutedRole, reason=reason)

@mute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    try:
        mutedRole = discord.utils.get(ctx.guild.roles, name="Canopus mute")
        await member.remove_roles(mutedRole)
        await member.send(f" you have unmuted from: - {ctx.guild.name}")
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Unmuted {member.mention}", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Roles")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@unmute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    valid = False
    warns = get_warns()
    for i in warns:
        if i[1] == ctx.guild.id:
            valid = True
            break
        else:
            valid = False
    if valid == False:
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:**` Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #1•Bot {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:2866zenitsuwtf:927951218733613086> `Case #1` {member.mention} has been warned.")
        add_warn(ctx.guild.id)
    else:
        add_amount(ctx.guild.id)
        amount = get_amount(ctx.guild.id)
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:** Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #{amount}•Bot {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:2866zenitsuwtf:927951218733613086>`Case #{amount}` {member.mention} has been warned.")

@warn.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    embed = discord.Embed(
        description=f"**Guild information for __{name}__**",
        color=discord.Color.blue()
        )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736>**Owner**", value=f"**{owner}**", inline=True)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736> **Channel Categories**", value=categories, inline=True)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736> **Text Channels**", value=text_channels, inline=True)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736> **Voice Channels**", value=voice_channels, inline=True)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736> **Members**", value=memberCount, inline=True)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736> **Region**", value=region, inline=True)
    embed.add_field(name="<a:6686arrowcyan:927951395280285736> **Boost Count**", value=ctx.guild.premium_subscription_count, inline=True)
    embed.set_footer(text=f"ID: {id} | Server Created • {ctx.guild.created_at.month}/{ctx.guild.created_at.day}/{ctx.guild.created_at.year}")
    embed.set_thumbnail(url=f"{icon}")
    """
    async with ctx.typing():
        await asyncio.sleep(3)
    """
    await ctx.send(embed=embed)

@client.command()
async def whois(ctx, user:discord.Member = None):
    if user is None:
        user = ctx.author
    if len(user.public_flags.all()) < 1:
        bage = None
    else:
        bage = str(user.public_flags.all()).replace('[<UserFlags.', '').replace('>]', '').replace('_',' ').replace(':', '').title()
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(description=f"""**User**
   <a:6686arrowcyan:927951395280285736>**Username:** {user}
   <a:6686arrowcyan:927951395280285736> **ID:** {user.id}
  <a:6686arrowcyan:927951395280285736> **Flags:** {bage}
  <a:6686arrowcyan:927951395280285736>**Avatar:** [Link to avatar]({user.avatar_url})
   <a:6686arrowcyan:927951395280285736>**Time Created:** {user.created_at.strftime(date_format)}
   <a:6686arrowcyan:927951395280285736> **Status:** {user.status}
  <a:6686arrowcyan:927951395280285736>**Game:** {user.activity}
    
    **Member**
   <a:6686arrowcyan:927951395280285736> **Highest Role:** {user.top_role}
   <a:6686arrowcyan:927951395280285736> **Server Join Date:** {user.joined_at.strftime(date_format)}
   <a:6686arrowcyan:927951395280285736>**Roles [{len(user.roles)-1}]:** {' '.join([r.mention for r in user.roles][1:])}""")
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, user : discord.Member, role : discord.Role):
    try:
        await user.add_roles(role)
        embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Updated roles for {user.mention}, **+ {role}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/aeE5OwMRMZyb0rPx9C8gbdWMMVz7tufjjYoNvEJOnVQ/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/861886912616988672/274ee804bfefa5c2f1dfd5a471de7c44.webp?width=341&height=341")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Roles")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@role.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_roles=True)
async def unrole(ctx, user : discord.Member, role : discord.Role):
    try:
        await user.remove_roles(role)
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Removed role from {user.mention}, **- {role}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@unrole.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,read_messages=False)
        embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Hided {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<a:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@hide.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unhide(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,read_messages=True)
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Unhided {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<a:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@unhide.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
        embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Locked {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@lock.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=True)
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Unlocked {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@unlock.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

def ConvertSectoDay(n):
 
    day = n // (24 * 3600)
 
    n = n % (24 * 3600)
    hour = n // 3600
 
    n %= 3600
    minutes = n // 60
 
    n %= 60
    seconds = n
     
    return (day,"days", hour, "hours",
          minutes, "minutes",
          seconds, "seconds")

@client.command()
async def gstart(ctx, time=None, winners =None, *, prize=None):
    has_role = False
    has_role1 = False
    role = discord.utils.find(lambda r: r.name == 'Giveaways', ctx.message.guild.roles)
    role = discord.utils.find(lambda r: r.name == 'giveaways', ctx.message.guild.roles)
    if role in ctx.author.roles:
        has_role = True
    if has_role1 in ctx.author.roles:
        has_role1 = True
    if ctx.author.guild_permissions.manage_channels or has_role == True or has_role1 == True:
        if time == None:
            return await ctx.channel.send("Please include a time!")
        elif prize == None:
            return await ctx.channel.send("Please include a prize!")
        time_converter = {"s":1, "m":60, "h":3600, "d":86400}
        t = time
        t = t.replace(f"{time[-1]}","")
        t = int(t)
        gawtime = int(t) * time_converter[time[-1]]
        await ctx.message.delete()
        w = gawtime
        ti = ConvertSectoDay(w)
        listx = list(ti)
        f = ""
        for i in listx:
            f += str(i) + " "
        embed = discord.Embed(
                title="<a:2659tadapurple:927951128065368064>  New Giveaway! <a:2659tadapurple:927951128065368064>",
                description=f"**Prize:** {prize}\n"
                            f"**Hosted By:** {ctx.author.mention}\n"
                            f"**Ends In:** {f}\n\n"
                            f"**__Giveaway Winners__**\n"
                            "Not Decided.\n\n"
                            "[Upvote me for 35% Good luck](https://top.gg/bot/924936306126106634) • [Invite me](https://discord.com/oauth2/authorize?client_id=924936306126106634&scope=bot%20applications.commands&permissions=8589934591)",
                colour=discord.Color.green()
            )
        winners = winners.replace(f"{winners[-1]}","")
        winners = int(winners)
        embed.set_footer(text=f"{winners} winner(s)!",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        gaw_msg = await ctx.channel.send(embed=embed)
        await gaw_msg.add_reaction("🎉")
        while w:
            await asyncio.sleep(10)
            w -= 10
            ti = ConvertSectoDay(w)
            f = ""
            listx = list(ti)
            for i in listx:
                f += str(i) + " "
            embed.description= f"**Prize:** {prize}\n**Hosted By:** {ctx.author.mention}\n**Ends In:** {f}\n\n**__Giveaway Winners__**\nNot Decided.\n\n[Upvote me for 20% Good luck](https://discordbotlist.com/bots/canopus/upvote) • [Invite me](https://discord.com/oauth2/authorize?client_id=924936306126106634&scope=bot%20applications.commands&permissions=8589934591)"
            await gaw_msg.edit(embed=embed)
        new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)
        users = await new_gaw_msg.reactions[0].users().flatten()
        if winners > 1:
            winner = random.choices(users, k=winners)
        else:
            winner = random.choice(users)
        embed.description= f"**Prize:** {prize}\n**Hosted By:** {ctx.author.mention}\n**Ends In:** {f}\n**__Giveaway Winners__**\n{winner.mention}."
        await gaw_msg.edit(embed=embed)
        await ctx.channel.send(f"<a:2659tadapurple:927951128065368064>  **Giveaway Winner: {winner.mention} | Prize: {prize} <a:2659tadapurple:927951128065368064> **")
    else:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels | Giveaways Roles")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)


@client.command()
@commands.has_permissions(manage_channels=True)
async def greroll(ctx, id_ = None):
    has_role = False
    role = discord.utils.find(lambda r: r.name == 'Giveaways', ctx.message.guild.roles)
    if role in ctx.author.roles:
        has_role = True
    if ctx.author.guild_permissions.manage_channels or has_role == True:
        if id_ == None:
            await ctx.channel.send("please enter giveaway id.")
        else:
            id_ = int(id_)
        try:
            new_msg = await ctx.channel.fetch_message(id_)
        except:
            await ctx.channel.send("The id was enterd incorrectly.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))

        winner = random.choice(users)
        await ctx.channel.send(f"<a:2659tadapurple:927951128065368064>  **New giveaway Winner: {winner.mention}**")
    else:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels | Giveaways Roles")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)


@client.command()
@commands.has_permissions(manage_channels=True)
async def gend(ctx, id_ = None):
    has_role = False
    role = discord.utils.find(lambda r: r.name == 'Giveaways',ctx.message.guild.roles)
    if role in ctx.author.roles:
        has_role = True
    if ctx.author.guild_permissions.manage_channels or has_role == True:
        if id_ == None:
            await ctx.channel.send("please enter giveaway id.")
        else:
            id_ = int(id_)
        try:
            new_msg = await ctx.channel.fetch_message(id_)
        except:
            await ctx.channel.send("The id was enterd incorrectly.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))
        winner = random.choice(users)
        await ctx.channel.send(f"<a:2659tadapurple:927951128065368064>  **Giveaway Winner:** {winner.mention}")
    else:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels | Giveaways Roles")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)


@client.command()
async def gif(ctx,*,q=None):
    if q == None:
        await ctx.channel.send("Provide name of gif, ,gif <name>")
    api_key="sPM0GnfKMOd5VhXXiHbB096gZpNarYWo"
    api_instance = giphy_client.DefaultApi()

    try:        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

@client.command()
async def greet(ctx):
    if ctx.author.guild_permissions.manage_channels:
        servers = get_greet()
        valid = False
        try:
            for i in servers:
                if i[2] == ctx.channel.id:
                    remove_greet(ctx.channel.id)
                    embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Disabled greet announcement on: {ctx.channel.mention}", color=0xFF0000)
                    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
                    await ctx.channel.send(embed=embed)
                    valid = True
                    break
        except:
            valid=False
        if valid == False:
            add_greet(ctx.guild.id,ctx.channel.id)
            embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Enabled greet announcement on: {ctx.channel.mention}", color=0x00FF00)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
            await ctx.channel.send(embed=embed)
    else:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)



@client.event
async def on_member_join(member):
    servers = get_greet()
    for i in servers:
        if i[1] == member.guild.id:
          try:
            channel = client.get_channel(i[2])
            msg = await channel.send(f"**Welcome {member.mention} in {member.guild.name}**")
            await asyncio.sleep(i[3])
            await msg.delete()
          except:
            pass

@greet.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
async def avatar(ctx, user:discord.Member = None):
    if user is None:
        user = ctx.author
    embed = discord.Embed(title="Avatar")
    embed.set_author(name=user,icon_url=user.avatar_url)
    embed.set_image(url=user.avatar_url)
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.channel.send(embed=embed)

@client.command()
async def say(ctx, *, msg):
    if ctx.author.id == 758697679667855433 or ctx.author.id == 827975272321777724: 
        embed = discord.Embed(description=msg,color=0x00FF00)
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Sorry but this command can only be accessed by the developer.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@client.command(aliases=['add'])
async def invite(ctx):
    embed = discord.Embed(
        description=f"""Use The `botinfo` For More Information About Our Bot
       <a:6686arrowcyan:927951395280285736> **Invite**
        [Invite me](https://discord.com/oauth2/authorize?client_id=924936306126106634&scope=bot%20applications.commands&permissions=8589934591)
      <a:6686arrowcyan:927951395280285736> **Support Server**
        [Join my support server](https://discord.gg/NjX9XuMACb)""",
        color=discord.Color.blue()
        )
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.send(embed=embed)

@client.command()
async def botinfo(ctx):
    members = 0
    for guild in client.guilds:
      members += guild.member_count
    embed = discord.Embed(color=discord.Color.blue())
    embed.add_field(name="**Version**",value="2.0.0")
    embed.add_field(name="**Users**",value=members)
    embed.add_field(name="**Servers**",value=str(len(client.guilds)))
    embed.add_field(name="**Discord.py Version**",value="1.7.2")
    embed.add_field(name="**Developers**",value="""**Gamecooler19#3016**""",inline=False)
    embed.add_field(name="\u200b",value="[Join my support server](https://discord.gg/NjX9XuMACb) • [Invite me](https://discord.com/oauth2/authorize?client_id=924936306126106634&scope=bot%20applications.commands&permissions=8589934591)")
    embed.set_thumbnail(url=str(ctx.guild.icon_url))
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.channel.send(embed=embed)

@client.command()
async def update(ctx,):
    if ctx.author.id == 758697679667855433:
        members = 0
        for guild in client.guilds:
            members += guild.member_count
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Watching {str(len(client.guilds))} Servers And {members} Users"))
    else:
        embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085>Sorry but this command can only be accessed by the developer.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@client.command()
async def economy(ctx):
    embed = discord.Embed(description=f"`c!balance` `c!beg` `c!bet` `c!daily` `c!share`", color=0xFF0000)
    embed.set_author(name=f"- Economy Commands",url="")
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.channel.send(embed=embed)

@client.command()
async def balance(ctx, user : discord.Member =None):
    users = get_users()
    if user is None:
        member = ctx.author
    if user is not None:
        member = user
    is_done = False
    for i in users:
        if i[1] == member.id:
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name=f"Canopus Bot  Economy",url="")
            embed.add_field(name="Balance",value=f"{member.name} has <a:2838dogecoin:927951161078714409>  **{i[2]}**")
            embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
            await ctx.channel.send(embed=embed)
            is_done = True
            break
    if is_done == False:
        add_user(member.id)
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f" Canopus Bot  Economy",url="")
        embed.add_field(name="Balance",value=f"{member.name} has <a:2838dogecoin:927951161078714409>  **0**")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    users = get_users()
    money = random.randint(100,1000)
    is_done = False
    for i in users:
        if i[1] == ctx.author.id:
            add_money(ctx.author.id,money)
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name=f" Canopus Bot  Economy",url="")
            embed.add_field(name="Begging!",value=f"**Broken Tooth** Donated <a:2838dogecoin:927951161078714409>  {money} to {ctx.author.mention}")
            embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
            await ctx.channel.send(embed=embed)
            is_done = True
            break
    if is_done == False:
        add_user(ctx.author.id)
        add_money(ctx.author.id,money)
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f" Canopus Bot  Economy",url="")
        embed.add_field(name="Begging!",value=f"**Broken Tooth** Donated <a:2838dogecoin:927951161078714409>  {money} to {ctx.author.mention}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):  
        return await ctx.send('The command **{}** is still on cooldown for {:.2f}'.format(ctx.command.name, error.retry_after))

@client.command()
async def share(ctx,user : discord.Member, money):
    users = get_users()
    is_done = False
    for i in users:
        if i[1] == user.id:
            is_done = True
    if is_done == False:
        add_user(user.id)
        is_done = True
    #if is_done1 and i[2] >= money and is_done:
    userf = get_info(int(ctx.author.id))
    if userf[2] > int(money):
        share_money(int(ctx.author.id),int(user.id),int(money))
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f" Canopus Bot  Economy",url="")
        embed.add_field(name="<:6609yes:927951013560856667> Sharing!",value=f"You shared <a:2838dogecoin:927951161078714409>  {money} coins to {user.mention}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    else:
         ctx.send(f"{ctx.author.mention}, You have insufficient balance!")

@client.command()
async def give(ctx,user : discord.Member, money):
    if ctx.author.id == 758697679667855433:
        users = get_users()
        is_done = False
        for i in users:
            if i[1] == user.id:
                is_done = True
        if is_done == False:
            add_user(user.id)
            is_done = True
        #if is_done1 and i[2] >= money and is_done:
        give_money(int(user.id),int(money))
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f" Canopus Bot  Economy",url="")
        embed.add_field(name="Sharing!",value=f"You gave <a:2838dogecoin:927951161078714409>  {money} coins to {user.mention}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    users = get_users()
    is_done = False
    for i in users:
        if i[1] == ctx.author.id:
            add_money(ctx.author.id,5000)
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name=f" Canopus Bot   Economy",url="")
            embed.add_field(name="Daily Reward",value=f"You got <a:2838dogecoin:927951161078714409>  **5000**")
            embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
            await ctx.channel.send(embed=embed)
            is_done = True
            break
    if is_done == False:
        add_user(ctx.author.id)
        add_money(ctx.author.id,5000)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def bet(ctx, amount = None):
    if str(amount) == None:
        embed2 = discord.Embed(color=0xFF0000)
        embed2.set_author(name=f" Canopus Bot  Economy",url="")
        embed2.add_field(name="Usage",value=f",bet <amount>")
        embed2.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed2)
    else:
        users = get_users()
        is_done = False
        listx = ["lose","win"]
        result = random.choice(listx)
        for i in users:
            if i[1] == ctx.author.id and int(i[2]) > int(amount):
                if result == "lose":
                    remove_money(ctx.author.id,int(amount))
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name=f"Canopus Bot  Economy",url="")
                    embed.add_field(name="You Lost!",value=f":cry: Awww.. you lost the bet <a:2838dogecoin:927951161078714409>  **{amount}**")
                    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
                    await ctx.channel.send(embed=embed)
                    is_done = True
                    break
                else:
                    give_money(ctx.author.id,int(amount)*2)
                    embed1 = discord.Embed(color=0x00FF00)
                    embed1.set_author(name=f" Canopus Bot  Economy",url="")
                    embed1.add_field(name="You Won!",value=f"<:6609yes:927951013560856667>   Congrats you have won the bet <a:2838dogecoin:927951161078714409>  **{int(amount)*2}**")
                    embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
                    await ctx.channel.send(embed=embed1)
                    is_done = True
                    break

    if is_done == False:
        add_user(ctx.author.id)


@client.command()
async def shop(ctx):
    embed = discord.Embed(color=0xFF0000)
    embed.set_author(name=f"Canopus Bot  Economy",url="")
    embed.add_field(name="Shop",value=f"**1.** Empathy Banana - <a:2838dogecoin:927951161078714409>  50000\n\n**2.** Rare Bitcoin - <a:2838dogecoin:927951161078714409>  500000\n\n**3.** Lamborghini - <a:2838dogecoin:927951161078714409> 25000\n\n**4.** Computer -<a:2838dogecoin:927951161078714409>  5000")
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.channel.send(embed=embed)


@client.command()
async def ping(ctx):
    embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Pong! {round(client.latency * 1000)}ms", color=0x00FF00)
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.channel.send(embed=embed)

@client.command(name="8ball", description="Show 8ball")
async def _8ball(ctx, *, question):
  responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
  result = random.choice(responses)
  await ctx.reply(f"🎱 {result}", mention_author=True)

@slash.slash(name="8ball")
async def __8ball(ctx, *, question):
  responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
  result = random.choice(responses)
  await ctx.send(f"🎱 {result}")

@slash.slash(name="hack")
async def hack(ctx, user : discord.Member):
    message = await ctx.send(f"Hacking {user} now...")
    words = ["Alpha is a terrible bot",]
    await asyncio.sleep(3)
    await message.edit(content="[**11.32%**] Finding discord login... (2fa bypassed)")
    await asyncio.sleep(3)
    await message.edit(content=f"[**18.19%**] Found:\n**Email:** `{user}*****@gmail.com`\n**Password:** `123456789`")
    await asyncio.sleep(3)
    await message.edit(content="[**24.05%**] Fetching dms with closet friends (if there are any friends at all)")
    await asyncio.sleep(3)
    await message.edit(content="[**28.65%**] **Last DM:** 'I hope no one sees my nudes folder'")
    await asyncio.sleep(3)
    await message.edit(content="[**37.65%**] Finding most common word...")
    await asyncio.sleep(3)
    await message.edit(content="[**44.62%**] `const mostCommonWord: string = 'meme';`")
    await asyncio.sleep(3)
    await message.edit(content=f"[**50.57%**] Injecting trojan virus into discriminator {user.discriminator}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**48.62%**] Virus injected, emotes stolen <:2866zenitsuwtf:927951218733613086>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**60.25%**] Hacking Epic Store account... <a:yes:867043585248985089>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.69**] Breached Epic Store Account: No More 19 Dollar Fortnite Cards 🚫")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.11%**] Finding IP address")
    await asyncio.sleep(3)
    await message.edit(content=f"[**76.65%**] **IP address:** 127.0.0.1.4292")
    await asyncio.sleep(3)
    await message.edit(content=f"[**90.27%**] Selling data to the Goverment...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**93.12%**] Reporting account to Discord for breaking TOS...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**95.70%**] Finished hacking {user}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**100%**] The **totally** real and dangerous hack is complete")

@client.command()
async def vote (ctx):
    embed = discord.Embed(title="Vote For Me", description="**Discord Bot List Vote Link :-** [DBL Vote](https://discordbotlist.com/bots/canopus/upvote)\n \n **Top.gg Vote Link :-** [Top.gg Vote](https://top.gg/bot/924936306126106634)", colour=discord.Colour.blue())
    await ctx.send(embed=embed)

@client.command()
async def hack(ctx, user : discord.Member):
    message = await ctx.send(f"Hacking {user} now...")
    words = ["dank memer is a terrible bot",]
    await asyncio.sleep(3)
    await message.edit(content="[**11.32%**] Finding discord login... (2fa bypassed)")
    await asyncio.sleep(3)
    await message.edit(content=f"[**18.19%**] Found:\n**Email:** `{user}*****@gmail.com`\n**Password:** `123456789`")
    await asyncio.sleep(3)
    await message.edit(content="[**24.05%**] Fetching dms with closet friends (if there are any friends at all)")
    await asyncio.sleep(3)
    await message.edit(content="[**28.65%**] **Last DM:** 'I hope no one sees my nudes folder'")
    await asyncio.sleep(3)
    await message.edit(content="[**37.65%**] Finding most common word...")
    await asyncio.sleep(3)
    await message.edit(content="[**44.62%**] `const mostCommonWord: string = 'meme';`")
    await asyncio.sleep(3)
    await message.edit(content=f"[**50.57%**] Injecting trojan virus into discriminator {user.discriminator}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**48.62%**] Virus injected, emotes stolen <a:yes:867043585248985089>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**60.25%**] Hacking Epic Store account... <a:yes:867043585248985089>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.69**] Breached Epic Store Account: No More 19 Dollar Fortnite Cards 🚫")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.11%**] Finding IP address")
    await asyncio.sleep(3)
    await message.edit(content=f"[**76.65%**] **IP address:** 127.0.0.1.4292")
    await asyncio.sleep(3)
    await message.edit(content=f"[**90.27%**] Selling data to the Goverment...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**93.12%**] Reporting account to Discord for breaking TOS...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**95.70%**] Finished hacking {user}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**100%**] The **totally** real and dangerous hack is complete")

@client.command()
async def greetdel(ctx,amount):
    if ctx.author.guild_permissions.manage_channels:
        servers = get_greet()
        valid = False
        try:
            for i in servers:
                if i[2] == ctx.channel.id:
                    update_greet(ctx.channel.id,int(amount))
                    embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Seted greet announcement on: {amount}s", color=0x00FF00)
                    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
                    await ctx.channel.send(embed=embed)
                    valid = True
                    break
        except:
            valid=False
        if valid == False:
            embed = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Greet command is not enabled on this channel", color=0xFF0000)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
            await ctx.channel.send(embed=embed)

@greetdel.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")


@client.command()
@commands.has_permissions(administrator=True)
async def joinchannel(ctx, channel = None):
    if channel is None:
        embed2 = discord.Embed(description=f"Mention channel. | c!joinchannel #channel", color=0xFF0000)
        embed2.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed2.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed2)
    servers = get_join_channels()
    valid = False
    a = channel.replace("<#","").replace(">","")
    for i in servers:
        if i[2] == int(a):
          valid = True
          break
    if valid == False:
        add_joinchannel(ctx.guild.id,int(a))
        embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Enabled joinchannel announcement on: {channel}", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed)
    else:
        embed1 = discord.Embed(description=f"<:1887crossbluepurple:927951094666113085> Join channel is already enabled. | write c!removejoinchannel to remove it.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
        await ctx.channel.send(embed=embed1)

@joinchannel.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")


@client.command()
@commands.has_permissions(administrator=True)
async def removejoinchannel(ctx, channel):
    if channel is None:
      embed2 = discord.Embed(description=f"Mention channel. | c!joinchannel #channel", color=0xFF0000)
      embed2.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
      embed2.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
      await ctx.channel.send(embed=embed2)
    a = channel.replace("<#","").replace(">","")
    remove_joinchannel(int(a))
    embed = discord.Embed(description=f"<:6609yes:927951013560856667>  Removed join channel.", color=0x00FF00)
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"| Canopus Bot |  {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://cdn.discordapp.com/avatars/924936306126106634/c8fdb784c74946f02442360ee137dfba.webp?size=1024")
    await ctx.channel.send(embed=embed)

@removejoinchannel.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")


extensions = ['cogs.invites']
if __name__ == '__main__':
    for ext in extensions:
       client.load_extension(ext)

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
             
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')
@client.command()
async def web (ctx):
    embed = discord.Embed(title="Website Link", description="[Check Out Our Website](https://gamecooler19.github.io/canopus.github.io/#/)", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Purged By {}'.format(ctx.author.mention), delete_after=3.0)
        await ctx.message.delete()

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")

@client.command()
@commands.has_permissions(kick_members=True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
  try:
    new_msg = await channel.fetch_message(id_)
  except:
    await ctx.send("The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))

  winner = random.choice(users)

  await channel.send(f"Congratulations the new winner is: {winner.mention} for the giveaway rerolled!")

@client.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    slowmode_embed = discord.Embed(title="Slowmode", description="A slowmode was set for this channel", colour=discord.Colour.green())
    await ctx.send(embed=slowmode_embed, delete_after=5.0)

@slowmode.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey , Mate You Don't Have Perm To Do That!")


@client.command()
async def embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Waiting for a title')
    title = await client.wait_for('message', check=check)
  
    await ctx.send('Waiting for a description')
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content,  color = discord.Colour.random())
    await ctx.send(embed=embed)



@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

killgifs = ['https://c.tenor.com/1dtHuFICZF4AAAAC/kill-smack.gif',
            'https://c.tenor.com/gQAWuiZnbZ4AAAAC/pokemon-anime.gif',
            'https://c.tenor.com/PJbU0yjG3BUAAAAd/anime-girl.gif',
            'https://c.tenor.com/Re9dglY0sCwAAAAC/anime-wasted.gif']


@client.command(name='kill')
async def kill(ctx, person: discord.Member): # Make the person a discord.Member
    author = ctx.author
    embed = discord.Embed(color=discord.Color.red())
    embed.set_author(name=f'{author} kills {person.display_name}') # Display the name
    embed.set_image(url=(random.choice(killgifs)))
    await ctx.send(embed=embed)

@client.command()
async def banner(ctx, user:discord.Member):
    if user == None:
        user = ctx.author
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    # If statement because the user may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
    await ctx.send(f"{banner_url}")   

async def timeout_user(*, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {client.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    async with client.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
           return True
        return False


@client.command()
async def timeout(ctx: commands.Context, member: discord.Member, until: int):
    handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until)
    if handshake:
         return await ctx.send(f"Successfully timed out user for {until} minutes.")
    await ctx.send("Something went wrong")

@client.command(aliases=['premium'])
async def buy(ctx):
    embed = discord.Embed(title="Canopus Premium", description="[Buy Canopus Premium](https://www.patreon.com/Canopus?fan_landing=true) \n \n **From This You Can Buy Canopus Premium And Support Developers**", colour=discord.Colour.green())
    await ctx.send(embed=embed)

client.add_cog(Music(client))

client.run("OTI0OTM2MzA2MTI2MTA2NjM0.Ycl0Dw.DSrsDP0SPZVSKb7t56cVI4OI6TQ")

