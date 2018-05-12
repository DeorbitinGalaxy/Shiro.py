import discord
import asyncio
from config import *
import time
from discord.ext import commands
import random, os
import aiohttp
import requests, json
import urllib
import math
import pickle
import progressbar
from links import *

description = "The official public Shiro Bot"
bot = commands.Bot(command_prefix=prefix, description=description)
bot.remove_command("help")

#     _______     _______ _   _ _____ ____  
#    | ____\ \   / / ____| \ | |_   _/ ___| 
#    |  _|  \ \ / /|  _| |  \| | | | \___ \ 
#    | |___  \ V / | |___| |\  | | |  ___) |
#    |_____|  \_/  |_____|_| \_| |_| |____/...........................

@bot.event
async def on_ready():
	print ("Bot Ready")
	print (bot.user.name + "#" + bot.user.discriminator)
	print ("ID " + bot.user.id)
	print (discord.__version__)
	print ("In {} servers\n".format(len(bot.servers)))
	bot.loop.create_task(loop_task())

@bot.event
async def loop_task():
	presence = ["{}help | Shiro Bot".format(prefix), "github.com/StrawHatHacker/Shiro"]
	await bot.wait_until_ready()
	counter=-1
	while not bot.is_closed:
		counter+=1
		x = random.choice(presence)
		print("Presence Changed to `{}`, bot is on for {} minutes, In {} servers".format(x, counter*(loop_time//60), len(bot.servers)))
		await bot.change_presence(game = discord.Game(name = x))
		await asyncio.sleep(loop_time)

@bot.event
async def on_command_completion(command, ctx):
	print("{} | {} | {} | {} | {}".format(command, ctx.message.author.name, ctx.message.server.name, ctx.message.channel.name, ctx.message.clean_content))

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if message.content.upper().startswith("LOVE"):
		await bot.send_message(message.channel, ":heartbeat:")
	await bot.process_commands(message)

@bot.event
async def on_command_error(error, ctx):
	if isinstance(error, commands.CommandOnCooldown):
		x = await bot.send_message(ctx.message.channel, "❌ Command is on cooldown, try again in {} seconds".format(int(error.retry_after)))
		await asyncio.sleep(5)
		await bot.delete_message(x)
	elif isinstance(error, commands.MissingRequiredArgument):
		x = await bot.send_message(ctx.message.channel, "Missing argument, **{}help** for help".format(prefix))
		await asyncio.sleep(5)
		await bot.delete_message(x)
	elif isinstance(error, commands.CommandNotFound):
		pass
	elif isinstance(error, commands.errors.CheckFailure):
		y = ctx.message.content.split(" ")	
		x = await bot.send_message(ctx.message.channel, "{} you dont have permission to use the **{}** command".format(ctx.message.author.mention, y[0]))
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		await bot.delete_message(x)

#        _    ____  __  __ ___ _   _ 
#       / \  |  _ \|  \/  |_ _| \ | |
#      / _ \ | | | | |\/| || ||  \| |
#     / ___ \| |_| | |  | || || |\  |
#    /_/   \_\____/|_|  |_|___|_| \_|............................

@bot.command(pass_context=True, no_pm=True, aliases=["Warn"])
async def warn(ctx, member, *, reason="none"):
	try:
		member = ctx.message.mentions[0]
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:		
		await bot.send_message(member, "{} You have been **warned** on server: **{}**, for **{}**\nPlease follow the server rules".format(member.mention, ctx.message.server.name, reason))
		await bot.say("**{}** has been warned".format(member.name))	
	except:
		await bot.say("{} You have been **warned** on server: **{}**, for **{}**\nPlease follow the server rules".format(member.mention, ctx.message.server.name, reason))

@bot.command(pass_context=True, no_pm=True, aliases=["Mute"])
@commands.has_permissions(mute_members=True)
async def mute(ctx, *, member):
	try:
		member = ctx.message.mentions[0]
	except IndexError:
		x = await bot.say("Please mention a user")
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		overwrite = discord.PermissionOverwrite()
		overwrite.send_messages = False
		await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)
		embed=discord.Embed(description = "{} has been **muted** on this channel!".format(member.mention), color = color_blue)
		await bot.say(embed=embed)
	except:
		await bot.say("I couldn't mute that member, do I have *Manage Channel* permissions ?")

@bot.command(pass_context=True, no_pm=True, aliases=["Unmute"])
@commands.has_permissions(mute_members=True)
async def unmute(ctx, *, member):
	try:
		member = ctx.message.mentions[0]
	except IndexError:
		x = await bot.say("Please mention a user")
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		overwrite = discord.PermissionOverwrite()
		overwrite.send_messages = None
		await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)
		embed=discord.Embed(description = "{} has been **unmuted** on this channel!".format(member.mention), color = color_blue)
		await bot.say(embed=embed)
	except:
		await bot.say("I couldn't unmute that member, do I have *Manage Channel* permissions ?")

@bot.command(pass_context=True, no_pm=True, aliases=["Kick"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member, *, reason="None specified"):
	try:
		member = ctx.message.mentions[0]
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		await bot.kick(member)
		embed=discord.Embed(description = "**{}** has been **Kicked** from **{}**. Reason: **{}**".format(member.name, ctx.message.server.name, reason), color = color_blue)
		await bot.say(embed=embed)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			x = await bot.say(ctx.message.author.mention + ", I cant kick a member of **similar** or **higher** rank than me")
			await asyncio.sleep(10)
			return await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Ban"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member, *, reason="None specified"):
	try:
		member = ctx.message.mentions[0]
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		await bot.ban(member, delete_message_days = 1)
		embed=discord.Embed(description = "**{}** has been **Banned** from **{}**. Reason: **{}**".format(member.name, ctx.message.server.name, reason), color = color_blue)
		await bot.say(embed=embed)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			x = await bot.say(ctx.message.author.mention + ", I can't ban a member of **similar** or **higher** rank than me")
			await asyncio.sleep(10)
			return await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Sban"])
@commands.has_permissions(ban_members=True)
async def sban(ctx, member, *, reason="None specified"):
	await bot.delete_message(ctx.message)
	try:
		member = ctx.message.mentions[0]
	except IndexError:
		return
	try:
		await bot.ban(member, delete_message_days=1)
		embed=discord.Embed(description = "**{}** has been **Silent banned** from **{}**. Reason: **{}**".format(member.name, ctx.message.server.name, reason), color = color_blue)
		await bot.send_message(ctx.message.author, embed=embed)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			x = await bot.send_message(ctx.message.author, ctx.message.author.mention + ", I can't ban a member of **similar** or **higher** than as me")
			await asyncio.sleep(10)
			return await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Ping"])
async def ping(ctx):
	try:
		pingtime = time.time()
		pingms = await bot.say("Pinging....... " + ctx.message.server.name)
		ping = (time.time() - pingtime) * 1000
		ping = int(ping)
		await bot.edit_message(pingms, "{}ms".format(ping))
	except:
		x = await bot.say("I couldn't ping your server :cry:")
		await asyncio.sleep(10)
		return await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["purge","Prune", "Purge"])
@commands.has_permissions(manage_messages=True)
async def prune(ctx, number):
	number = int(number)
	if number>99:
		return await bot.say("Thats beyond my deleting powers, the maximum is 99")
	try:
		mgs = []
		number+=1
		async for x in bot.logs_from(ctx.message.channel, limit = number):
			mgs.append(x)
		await bot.delete_messages(mgs)
		await bot.say("`{}` messages deleted from **{}**".format(number-1, ctx.message.author.name))
	except:
		x = await bot.say("I couldn't prune `{}` messages :cry: do I have *Manage Messages* permission?".format(number-1))
		await asyncio.sleep(10)
		return await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Bans", "Banlist", "banlist"])
@commands.has_permissions(manage_server=True)
async def bans(ctx):
	try:	
		x = await bot.get_bans(ctx.message.server)
		x = "\n".join([y.name for y in x])
		embed=discord.Embed(title = "List", description = x, color = color_blue)
		await bot.say(embed=embed)
	except:
		x = await bot.say("I couldn't fetch your server's banned members")
		await asyncio.sleep(10)
		return await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Spam"])
@commands.has_permissions(manage_server=True)
async def spam(ctx):
	try:
		overwrite=discord.PermissionOverwrite()
		overwrite.send_messages=False
		await bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role, overwrite)
		embed=discord.Embed(description = "Channel {} has been muted, type `>nospam` in that channel to unmute it".format(ctx.message.channel.name), color = color_blue)
		await bot.send_message(ctx.message.author, embed=embed)
	except:
		await bot.say("I couldn't mute this channel, do I have *Manage Channel* permissions ?")

@bot.command(pass_context=True, no_pm=True, aliases=["Nospam"])
@commands.has_permissions(manage_server=True)
async def nospam(ctx):
	try:
		overwrite=discord.PermissionOverwrite()
		overwrite.send_messages=None
		await bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role, overwrite)
		embed=discord.Embed(description = "Channel {} has been unmuted".format(ctx.message.channel.name), color = color_blue)
		await bot.send_message(ctx.message.author, "Channel {} has been unmuted".format(ctx.message.channel.name))
	except:
		await bot.say("I couldn't unmute unmute this channel, do I have *Manage Channel* permissions ?")

@bot.command(pass_context = True, no_pm = True)
@commands.has_permissions(administrator=True)
@commands.cooldown(10,30)
async def serverinfo(ctx):
	server = ctx.message.server
	roles = [x.name for x in server.role_hierarchy]
	role_length = len(roles)
	roles = ', '.join(roles)
	channels = len(server.channels);
	time = str(server.created_at); time = time.split(' '); time= time[0];
	embed=discord.Embed(description = "Info on this server", title = ':thinking:', color = color_blue)
	embed.set_thumbnail(url = server.icon_url)
	embed.add_field(name = '__Server __', value = str(server))
	embed.add_field(name = '__Server ID__', value = str(server.id))
	embed.add_field(name = '__Owner__', value = str(server.owner))
	embed.add_field(name = '__Owner ID__', value = server.owner.id)
	embed.add_field(name = '__Members__', value = str(server.member_count))
	embed.add_field(name = '__Text/Voice Channels__', value = str(channels))
	embed.add_field(name = '__Roles__', value = '%s'%str(role_length))
	embed.add_field(name = '__Server Region__', value = '%s'%str(server.region))
	embed.add_field(name = '__AFK Channel__', value = server.afk_channel)
	embed.add_field(name = '__Verification Level__', value = server.verification_level)
	embed.add_field(name = '__Created on__', value = server.created_at.__format__('Date - %d %B %Y at time - %H:%M:%S'))
	await bot.say(embed=embed)

#      ____                           
#     / ___| __ _ _ __ ___   ___  ___ 
#    | |  _ / _` | '_ ` _ \ / _ \/ __|
#    | |_| | (_| | | | | | |  __/\__ \
#     \____|\__,_|_| |_| |_|\___||___/...............................

@bot.command(no_pm=True, aliases=["Team"])
async def team(*, message:str):
	try:
		msg = []
		arr = []
		msg = message.split(" ")
		random.shuffle(msg, random.random)
		for i in range(len(msg)//2):
			arr.append(msg[i])
			msg.pop(i)
		team1 = "\n".join(msg)
		team2 = "\n".join(arr)
		embed=discord.Embed(description = "**Team Maker 101**", color = color_blue)
		embed.add_field(name = "Team 1", value = team1)
		embed.add_field(name = "Team 2", value = team2)
		await bot.say(embed=embed)
	except:
		await bot.say("Give at least 2 arguments after the command")

@bot.command(pass_context=True, no_pm=True, aliases=['8ball', "Ball", "8Ball"])
async def ball(ctx, *, message):
	answers=["Better not tell you ", "Yes ", "No ", "Im not sure", "Definitely", "Hell no ", "I don't know ", "Just leave me alone "]
	embed=discord.Embed(title = message, description = answers[random.randint(0, len(answers))-1] + ctx.message.author.name, color = color_blue)
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases = ["Ship"])
async def ship(ctx, word1, word2):
	val1=0
	val2=0
	for i in range(len(word1)):
		val1 += ord(word1[i])
	for i in range(len(word2)):
		val2 += ord(word2[i])
	val = (val1 + val2) * (val1 + val2)
	while val>200:
		val = int(val/2)
	val-=100
	ans = progressbar.update_progress((val)/100)
	if val<25:
		resp = "So bad :cry:"
	elif val<50:
		resp = "Oof :grimacing:"
	elif val<75:
		resp = "Nice :smile:"
	else:
		resp = "Omg :astonished:"	
	embed=discord.Embed(title = resp, description = "Ship **{}** x **{}**\n{}".format(word1, word2, ans) , color = color_blue)
	embed.set_author(name = ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["Dice"])
async def dice(ctx):
	embed = discord.Embed(color = color_blue)
	embed.set_author(name = ctx.message.author.name)
	embed.add_field(name = 'RESULT', value = str(random.randint(1,6)))
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["Embed"])
async def embed(ctx, *, message:str):
	embed = discord.Embed(color = color_blue)
	embed.set_author(name = ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
	embed.description = message
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.command(pass_context=True, no_pm=True, aliases=["Say"])
async def say(ctx, *, message):
	x = message
	await bot.delete_message(ctx.message)
	await bot.say(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Rps"])
async def rps(ctx, *, message):
	ans = ["rock", "paper", "scissors"]
	pick=ans[random.randint(0, 2)]
	embed=discord.Embed(title = "Bot VS {}".format(ctx.message.author.name), color = color_blue)
	embed.set_author(name = ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
	if message.lower() != ans[0] and message.lower() != ans[1] and message.lower() != ans[2] :
		return await bot.say("Pick Rock Paper or Scissors")
	elif message.lower() == pick:
		embed.add_field(name = "Its a draw!", value = "Bot picked {} too!".format(pick))
		return await bot.say(embed=embed)
	else:
		if message.lower()  == "rock" and pick == "paper":
			embed.add_field(name = "Bot Wins!", value = "Bot picked {}!".format(pick))
			await bot.say(embed=embed)
		elif message.lower()  == "rock" and pick == "scissors":
			embed.add_field(name = "{} Wins!".format(ctx.message.author.name), value = "Bot picked {}!".format(pick))
			await bot.say(embed=embed)
		elif message.lower()  == "paper" and pick == "rock":
			embed.add_field(name = "{} Wins!".format(ctx.message.author.name), value = "Bot picked {}!".format(pick))
			await bot.say(embed=embed)
		elif message.lower()  == "paper" and pick == "scissors":
			embed.add_field(name = "Bot Wins!", value = "Bot picked {}!".format(pick))
			await bot.say(embed=embed)
		elif message.lower()  == "scissors" and pick == "rock":
			embed.add_field(name = "Bot Wins!", value = "Bot picked {}!".format(pick))
			await bot.say(embed=embed)
		else:
			embed.add_field(name = "{} Wins!".format(ctx.message.author.name), value = "Bot picked {}!".format(pick))
			await bot.say(embed=embed)

#     _   _ _____ ___ _     ___ _______   __
#    | | | |_   _|_ _| |   |_ _|_   _\ \ / /
#    | | | | | |  | || |    | |  | |  \ V / 
#    | |_| | | |  | || |___ | |  | |   | |  
#     \___/  |_| |___|_____|___| |_|   |_|.................................
									   
@bot.command(pass_context=True, no_pm=True, aliases=["Help", "h", "H"])
async def help(ctx):
	embed=discord.Embed(description = "For further help visit our github: github.com/StrawHatHacker/Shiro\nPrefix: '{}'".format(prefix), color = color_blue)
	embed.set_author(icon_url = ctx.message.server.icon_url, name = "Hi!!!, you asked for help".format(ctx.message.server.name))
	embed.add_field(name = "Owner Commands", value = "`setgame`")
	embed.add_field(name = "Admin/Mod Commands", value = "`ban`, `sban`, `kick`, `warn`, `mute`, `unmmute`, `ping`, `prune`, `bans`, `serverinfo`")
	embed.add_field(name = "Reactions", value = "`cute`, `kiss`, `hug`, `pat`, `slap`, `blush`, `lick`, `mad`, `scared`, `tired`, `cry`, `nimu`, `tickle`, `run`, `bite`, `plot`, `nervous`, `poke`, `pout`, `pinch`")
	embed.add_field(name = "Games", value = "`team`, `8ball`, `ship`, `dice`, `embed`, `say`, `rps`")
	embed.add_field(name = "Utility", value = "`help`, `aes`, `aesb`, `aesi`, `aesib`, `intel`, `invite`")
	embed.add_field(name = "Fun", value = "`dog`, `doggo`, `shibe`, `cat`, `bird`, `fox`, `lizard`, `movie`, `urban`, `poll`, `chuck`, `joke`, `yesno`, `fakeid`, `randomavatar`")
	embed.add_field(name = "Math", value = "`add`, `sub`, `mult`, `div`, `power`, `sqr`, `log`, `pi`")
	embed.add_field(name = "Nsfw", value = "`rule34`, `yandere`, `danbooru`, `gelbooru`, `xbooru`, `realbooru`, `gif`")
	embed.add_field(name = "Dangerous Commands", value = "`spam`, `nospam`")
	try:
		await bot.send_message(ctx.message.author, embed=embed)
	except:
		await bot.say("I could not dm you the help embed {}".format(ctx.message.author.mention))

@bot.command(pass_context=True, no_pm=True, aliases=["Aes"])
async def aes(ctx, *, message:str):
	arr=[]
	message = str(message)
	for i in range (len(message)):
		arr.append(message[i])
	await bot.say(" ".join(arr))

@bot.command(pass_context=True, no_pm=True, aliases=["Aesb"])
async def aesb(ctx, *, message:str):
	arr=[]
	message = str(message)
	for i in range (len(message)):
		arr.append(message[i])
	await bot.say("**" + " ".join(arr) + "**")

@bot.command(pass_context=True, no_pm=True, aliases=["Aesi"])
async def aesi(ctx, *, message:str):
	arr=[]
	message = str(message)
	for i in range (len(message)):
		arr.append(message[i])
	await bot.say("*" + " ".join(arr) + "*")

@bot.command(pass_context=True, no_pm=True, aliases=["aesbi", "Aesbi", "Aesib"])	
async def aesib(ctx, *, message:str):
	arr=[]
	message = str(message)
	for i in range (len(message)):
		arr.append(message[i])
	await bot.say("***" + " ".join(arr) + "***")

@bot.command(pass_context=True, no_pm=True, aliases=["intellectify"])
async def intel(ctx, *, message:str):
	string = ""
	for x in message:
		string += random.choice([x.upper(), x.lower()])
	embed=discord.Embed(description = string, color = color_blue)
	embed.set_image(url = "https://pbs.twimg.com/media/C_ZudDVWsAAojma.jpg")
	await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.cooldown(5, 30)
async def invite(ctx):
	embed=discord.Embed(title = "Here is the bot's invite link **{}**!".format(ctx.message.author.name),\
	description = bot_invite_link, color = color_blue)
	await bot.say(embed=embed)

#     _____ _   _ _   _ 
#    |  ___| | | | \ | |
#    | |_  | | | |  \| |
#    |  _| | |_| | |\  |
#    |_|    \___/|_| \_|.........................................

@bot.command(pass_context=True, no_pm=True, aliases=["Movie"])
async def movie(ctx, *, name:str=None):
	await bot.send_typing(ctx.message.channel)
	if name is None:
		embed=discord.Embed(description = "Please specify a movie, *eg. >movie Inception*", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	key = "4210fd67"
	url = "http://www.omdbapi.com/?t={}&apikey={}".format(name, key)
	response = requests.get(url)
	x = json.loads(response.text)
	embed=discord.Embed(title = "**{}**".format(name).upper(), description = "Here is your movie {}".format(ctx.message.author.name), color = color_blue)
	if x["Poster"] != "N/A":
		embed.set_thumbnail(url = x["Poster"])
	embed.add_field(name = "__Title__", value = x["Title"])
	embed.add_field(name = "__Released__", value = x["Released"])
	embed.add_field(name = "__Runtime__", value = x["Runtime"])
	embed.add_field(name = "__Genre__", value = x["Genre"])
	embed.add_field(name = "__Director__", value = x["Director"])
	embed.add_field(name = "__Writer__", value = x["Writer"])
	embed.add_field(name = "__Actors__", value = x["Actors"])
	embed.add_field(name = "__Plot__", value = x["Plot"])
	embed.add_field(name = "__Language__", value = x["Language"])
	embed.add_field(name = "__Imdb Rating__", value = x["imdbRating"]+"/10")
	embed.add_field(name = "__Type__", value = x["Type"])
	embed.set_footer(text = "Information from the OMDB API")
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["Dog"])
async def dog(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "https://dog.ceo/api/breeds/image/random"
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(color = color_blue)
		embed.set_author(name =  "Here's Your Dog {}".format(ctx.message.author.name), icon_url = ctx.message.author.avatar_url)
		embed.set_image(url = data["message"])
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **dog** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Shibe"])
async def shibe(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(color = color_blue)
		embed.set_author(name =  "Here's Your Shibe {}".format(ctx.message.author.name), icon_url = ctx.message.author.avatar_url)
		embed.set_image(url = data[0])
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **shibe** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Cat"])
async def cat(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "http://shibe.online/api/cats?count=1&urls=true&httpsUrls=false"
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(color = color_blue)
		embed.set_author(name =  "Here's Your Cat {}".format(ctx.message.author.name), icon_url = ctx.message.author.avatar_url)
		embed.set_image(url = data[0])
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **cat** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Bird"])
async def bird(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "http://shibe.online/api/birds?count=1&urls=true&httpsUrls=false"
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(color = color_blue)
		embed.set_author(name =  "Here's Your Bird {}".format(ctx.message.author.name), icon_url = ctx.message.author.avatar_url)
		embed.set_image(url = data[0])
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **bird** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Fox"])
async def fox(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "https://randomfox.ca/floof"
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(color = color_blue)
		embed.set_author(name =  "Here's Your Fox {}".format(ctx.message.author.name), icon_url = ctx.message.author.avatar_url)
		embed.set_image(url = data["image"])
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **fox** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["liz"])
async def lizard(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "https://testy.nekos.life/api/v2/img/lizard"
		response = requests.get(url)
		data = json.loads(response.text)
		link = data["url"]
		embed=discord.Embed(color = color_blue)
		embed.set_author(name =  "Here's Your Lizard {}".format(ctx.message.author.name), icon_url = ctx.message.author.avatar_url)
		embed.set_image(url = link)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **lizard** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Urban"])
async def urban(ctx, *, msg:str):
	await bot.send_typing(ctx.message.channel)
	try:
		word = ' '.join(msg)
		api = "http://api.urbandictionary.com/v0/define"
		response = requests.get(api, params=[("term", word)]).json()
		if len(response["list"]) == 0:
			return await bot.say("Could not find that word!")
		embed = discord.Embed(title = "🔍 Search Word", description = word, color = color_blue)
		embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
		embed.add_field(name = "Examples:", value = response['list'][0]["example"])
		embed.set_footer(text = "Tags: " + ', '.join(response['tags']))
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **urban** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Chuck"])
async def chuck(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "http://api.icndb.com/jokes/random"
		response = requests.get(url)
		data = json.loads(response.text)
		value = data["value"]
		joke = value["joke"]
		embed=discord.Embed(description = joke, color = color_blue)
		embed.set_author(name = ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **chuck** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Joke"])
async def joke(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_ten"
		response = requests.get(url)
		data = json.loads(response.text)
		data = data[random.randint(0, 9)]
		embed=discord.Embed(description = "{}\n{}".format(data["setup"], data["punchline"]), color = color_blue)
		embed.set_author(name = ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **joke** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Yesno", "noyes", "Noyes"])	
async def yesno(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "https://yesno.wtf/api"	
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(description = "I say {} {}!".format(data["answer"].upper(), ctx.message.author.name), color = color_blue)
		embed.set_image(url = data["image"])
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **yesno** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Fakeid", "fi", "Fi"])
async def fakeid(ctx):
	await bot.send_typing(ctx.message.channel)
	try:
		url = "http://uinames.com/api/?ext"
		response = requests.get(url)
		data = json.loads(response.text)
		embed=discord.Embed(title = "All information listed is fake and random", color = color_blue)
		embed.set_footer(text = "Information from http://uinames.com/api/")
		embed.add_field(name = "Name: {} {}".format(data["name"], data["surname"]), value = "Gender: {}\nRegion: {}\nAge: {}\nPhone: {}\nEmail: {}\nPassword: {}".format(data["gender"], data["region"], data["age"], data["phone"], data["email"], data["password"]))
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **fakeid** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Randomavatar", "ra", "Ra"])
async def randomavatar(ctx, tag:str):
	try:
		await bot.say("Choose background **1** or **2** or **0** for empty")
		bg = await bot.wait_for_message(timeout = 10, author=ctx.message.author, channel=ctx.message.channel)
		if bg.content not in ["0", "1", "2"]:
			return await bot.say("Choose between 0, 1, 2, run the command again!")
		await bot.say("Choose style **1 2 3 4 **")
		st = await bot.wait_for_message(timeout = 10, author=ctx.message.author, channel=ctx.message.channel)
		if st.content not in ["1", "2", "3", "4"]:
			return await bot.say("Choose between **1 2 3 4**, run the command again!")
		url = "https://robohash.org/{}.png?bgset=bg{}&set=set{}".format(tag, bg.content, st.content)
		embed=discord.Embed(description = "Random Avatar UwU", color = color_blue)
		embed.set_image(url=url)
		embed.set_author(name = ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
		embed.set_footer(text = "From robohash.org")
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **randomavatar** command or you took too much time to answer")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Poll"])
async def poll(ctx, *, message):
	await bot.send_typing(ctx.message.channel)
	try:
		embed=discord.Embed(description = message, color = color_blue)
		embed.set_author(name = "Poll from " + ctx.message.author.name, icon_url = ctx.message.author.avatar_url)
		x = await bot.say(embed=embed)
		await bot.add_reaction(x, "👍")
		await bot.add_reaction(x, "\U0001f937")
		await bot.add_reaction(x, "👎")
	except:
		x = await bot.say("Sorry, there was an error with the **poll** command, do i have the *add reactions* permission?")
		await asyncio.sleep(5)
		await bot.delete_message(x)

#     ____  _____    _    ____ _____ ___ ___  _   _ ____  
#    |  _ \| ____|  / \  / ___|_   _|_ _/ _ \| \ | / ___| 
#    | |_) |  _|   / _ \| |     | |  | | | | |  \| \___ \ 
#    |  _ <| |___ / ___ \ |___  | |  | | |_| | |\  |___) |
#    |_| \_\_____/_/   \_\____| |_| |___\___/|_| \_|____/...................

@bot.command(pass_context=True, no_pm=True, aliases=["Cute"])
async def cute(ctx):
	try:
		y = random.choice(links_cute)
		await bot.send_typing(ctx.message.channel)
		embed=discord.Embed(description = "Here is a cute anime girl for you {}!".format(ctx.message.author.name), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **cute** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Kiss"])
async def kiss(ctx, *, member=""):
	try:
		indexTest = ctx.message.mentions[0]
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		y = random.choice(links_kiss)
		embed=discord.Embed(description = "{} kissed {}! Cute :3".format(ctx.message.author.mention, members), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **kiss** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Hug", "huggle", "Huggle"])
async def hug(ctx, *, member=""):
	try:
		indexTest = ctx.message.mentions[0]
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		y = random.choice(links_hug)
		embed=discord.Embed(description = "{} hugged {} tightly, awww!".format(ctx.message.author.mention, members), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **hug** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Pat"])
async def pat(ctx, *, member=""):
	try:
		indexTest = ctx.message.mentions[0]
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		y = random.choice(links_pat)
		embed=discord.Embed(description = "{} patted {} UwU!".format(ctx.message.author.mention, members), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **pat** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Slap"])
async def slap(ctx, *, member):
	try:
		indexTest = ctx.message.mentions[0]
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x) 
	try:
		y = random.choice(links_slap)
		embed=discord.Embed(description = "{} slapped {}!, hmmm".format(ctx.message.author.mention, members), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **slap** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Blush"])
async def blush(ctx):
	try:
		y = random.choice(links_blush)
		embed=discord.Embed(description = "{} blushed!".format(ctx.message.author.mention), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **blush** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Lick"])
async def lick(ctx, *, member=""):
	try:
		indexTest = ctx.message.mentions[0]
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
	except IndexError:
		x = await bot.say("Please mention a user")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		y = random.choice(links_lick)
		embed=discord.Embed(description = "{} licked {}, mmm tasty!".format(ctx.message.author.mention, members), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **lick** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Mad", "Angry", "angry"])
async def mad(ctx, *, member=""):
	try:
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_mad)
		if members == "":
			embed=discord.Embed(description = "{} is mad for some reason!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "{} is mad cause of {}! Better do something!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **mad/angry** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Scared"])
async def scared(ctx, *, member=""):
	try:
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_scared)
		if members == "":
			embed=discord.Embed(description = "{} is scared for some reason!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "{} is scared of {}!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **scared** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Tired"])
async def tired(ctx):
	try:
		y = random.choice(links_tired)
		embed=discord.Embed(description = "{} feels so tired!".format(ctx.message.author.mention), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **tired** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Cry"])
async def cry(ctx, *, member=""):
	try:
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_cry)
		if members == "":
			embed=discord.Embed(description = "{} is crying for some reason!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "{} is crying cause of {}!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **cry** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Nimu"])
async def nimu(ctx):
	try:
		url = ["https://media.giphy.com/media/ruYMwmyOtpIxa/giphy.gif"]
		y = random.choice(links)
		embed=discord.Embed(description = "Nimu nimu nimu nimu nimu nimu nimu nimu!\nhttps://www.youtube.com/watch?v=K-6XHtMFP5Q", color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **nimu** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Tickle"])
async def tickle(ctx, *, member=""):
	try:
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_tickle)
		if member == "":
			embed=discord.Embed(description = "I will tickle you {}, hihihi!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "{} is tickling {}, hihihi!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **tickle** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Run"])
async def run(ctx):
	try:
		y = random.choice(links_run)
		embed=discord.Embed(description = "{} is running so fast".format(ctx.message.author.name), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **run** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Bite"])
async def bite(ctx, *, member=""):
	try:
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_bite)
		if member == "":
			embed=discord.Embed(description = "I will bite you hard {}, aaaarg!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "{} is biting {}, kinky!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **bite** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Plot"])
async def plot(ctx):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	try:
		y = random.choice(links_plot)
		embed=discord.Embed(description = "Here is an anime with some thicc **plot** {}!".format(ctx.message.author.mention), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **plot** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Nervous"])
async def nervous(ctx):
	try:
		y = random.choice(links_nervous)
		embed=discord.Embed(description = "{} is so nervous".format(ctx.message.author.mention), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **nervous** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Poke"])
async def poke(ctx, *, member=""):
	try:		
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_poke)
		if member == "":
			embed=discord.Embed(description = "I poked you {}! hihi!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "{} pokes {}!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **poke** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Pout"])
async def pout(ctx):
	try:
		y = random.choice(links_pout)
		embed=discord.Embed(description = "{} pouted!".format(ctx.message.author.mention), color = color_blue)
		embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **pout** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

@bot.command(pass_context=True, no_pm=True, aliases=["Pinch"])
async def pinch(ctx, *, member=""):
	try:
		members = ""
		for member in ctx.message.mentions:
			members += " " + member.mention
		y = random.choice(links_pinch)
		if member == "":
			embed=discord.Embed(description = "Pinching {} is so much fun!".format(ctx.message.author.mention), color = color_blue)
			embed.set_image(url = y)
		else:
			embed=discord.Embed(description = "Ohh, {} pinched {}!".format(ctx.message.author.mention, members), color = color_blue)
			embed.set_image(url = y)
		await bot.say(embed=embed)
	except:
		x = await bot.say("Sorry, there was an error with the **pinch** command")
		await asyncio.sleep(5)
		await bot.delete_message(x)

#     _   _ ____  _______        __
#    | \ | / ___||  ___\ \      / /
#    |  \| \___ \| |_   \ \ /\ / / 
#    | |\  |___) |  _|   \ V  V /  
#    |_| \_|____/|_|      \_/\_/................................

@bot.command(pass_context=True, no_pm=True, aliases=["r", "r34", "rule"])
@commands.cooldown(3, 5)
async def rule34(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	limit = 100
	if message==None:
		listu = ["anime", "ass", "boobs", "anal", "pussy", "thighs", "yaoi", "yuri", "bdsm"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, message)
	try:
		response = requests.get(url)
		data = json.loads(response.text)
		limit = len(data)
	except json.JSONDecodeError:
		embed=discord.Embed(description = "Couldn't find a picture with that tag or there was a server problem", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = "http://img.rule34.xxx/images/{}/{}".format(x["directory"], x["image"])
	embed=discord.Embed(title = "Enjoy {}, lewd!!!".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From Rule34, Tag: {}, Results found: {}".format(message, limit))
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["yan"])
@commands.cooldown(3, 5)
async def yandere(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	limit = 100
	if message==None:
		listu = ["pantsu", "swimsuits", "dress", "breasts", "animal ears", "open shirt", "bra", "no bra", "cameltoe", "loli"\
				" thighhighs", "cleavage", "nipples", "ass", "bikini", "naked", "pussy", "panty pull", "see through", "underboob"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://yande.re/post/index.json?limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = x["file_url"]
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From yande.re, Tag: {}, Results found: {}".format(message, limit))
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["dan"])
@commands.cooldown(3, 5)
async def danbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	limit = 100
	if message==None:
		listu = ["breasts", "blush", "skirt", "thighhighs", "large breasts", "underwear", "panties"\
				"nipples", "ass", "pantyhose", "nude", "pussy"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://danbooru.donmai.us/post/index.json?limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	x = data[random.randint(0, limit-1)]
	if x["file_url"].startswith("http"):
		final_url = x["file_url"]
	else:
		final_url = "http://danbooru.donmai.us{}".format(x["file_url"])
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From danbooru, Tag: {}, Results found: {}".format(message, limit))
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["gel"])
@commands.cooldown(3, 5)
async def gelbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	limit = 100
	if message==None:
		listu = ["ass", "breasts", "cameltoe", "long hair", "female", "pussy", "nude", "on bed"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit,message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = x["file_url"]
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From gelbooru, Tag: {}, Results found: {}".format(message, limit))
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["xb"])
@commands.cooldown(3, 5)
async def xbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	limit = 100
	if message==None:
		listu = ["ass", " breasts", "pussy", "female", "nude", "bdsm", "spanking"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://xbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = "http://img3.xbooru.com/images/{}/{}".format(x["directory"], x["image"])
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From xbooru, Tag: {}, Results found: {}".format(message, limit))
	await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True, aliases=["rb"])
@commands.cooldown(10, 10)
async def realbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	limit = 100
	if message==None:
		listu = ["ass", " breasts", "pussy", "female", "nude", "bdsm", "spanking"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://realbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await bot.say(embed=embed)
		await asyncio.sleep(5)
		return await bot.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = "https://realbooru.com/images/{}/{}".format(x["directory"], x["image"])
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From realbooru, Tag: {}, Results found: {}".format(message, limit))
	await bot.say(embed=embed)

#     __  __       _   _     
#    |  \/  | __ _| |_| |__  
#    | |\/| |/ _` | __| '_ \ 
#    | |  | | (_| | |_| | | |
#    |_|  |_|\__,_|\__|_| |_|....................................

@bot.command()
async def add(x:int, y:int):
	await bot.say(x + y)
@bot.command()
async def sub(x:int, y:int):
	await bot.say(x - y)
@bot.command()
async def mult(x:int, y:int):
	await bot.say(x*y)
@bot.command()
async def div(x:int, y:int):
	await bot.say(x / y)
@bot.command()
async def power(x:int, y:int):
	await bot.say(x ** y)
@bot.command()
async def sqr(x:int):
	await bot.say(int(math.sqrt(x)))
@bot.command()
async def log(x:int, base:int):
	await bot.say(math.log(x,base))
@bot.command()
async def pi():
	await bot.say(math.pi)

#      _____        ___   _ _____ ____  
#     / _ \ \      / / \ | | ____|  _ \ 
#    | | | \ \ /\ / /|  \| |  _| | |_) |
#    | |_| |\ V  V / | |\  | |___|  _ < 
#     \___/  \_/\_/  |_| \_|_____|_| \_\........................

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def setgame(ctx, *, game:str):
	if ctx.message.author.id in owner_ids:
		try:
			await bot.change_presence(game=discord.Game(name=game))
		except Exception as e:
			print("Failed to set game: {}".format(str(e)))
	else:
		x = await bot.say("You are not the bot owner!")
		await asyncio.sleep(5)
		await bot.delete_message(x)

bot.run(token, bot=True, reconnect=True)