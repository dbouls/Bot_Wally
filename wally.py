import discord
from discord.ext import commands

# Discord Bot token
TOKEN = 'INSERT YOUR BOT TOKEN HERE'

#Prefix to wake up Wally
client = commands.Bot(command_prefix='!')

#Removes the Py Help Command that can be invoked through the bot
client.remove_command('help')

# Variable that tracks the win/loss bonus
position = 1

# Console message that Wally has connected to the server
@client.event
async def on_ready():
	print('Wally is Ready.')
	
# Changes Wally's status to "Watching for !help"
# type=1 playing
# type=2 listening
# type=3 watching
@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name="for !help", type=3))

# Discord Command "ping" to see if Wally is alive
@client.command()
async def ping():
	await client.say('Pong!')

# Wally responses depending on the loss bonus level
async def loss0():
	await client.say('No loss Bonus!')
	embed = discord.Embed(
		title=' ',
		colour=discord.Color.dark_green()
	)
	embed.set_author(name='No Loss Bonus')
	embed.add_field(
		name='Where we are',
		value='```No Bonus: $1400```\n1 Loss: $1900\n2 Losses: $2400\n3 Losses: $2900\nMax Loss: $3400', inline=True)
	await client.say(embed=embed)

async def loss1():
	await client.say('1 Round Loss Bonus - $1900')
	embed = discord.Embed(
		title=' ',
		colour=discord.Color.gold()
	)
	embed.set_author(name='1 Loss Bonus')
	embed.add_field(
		name='Where we are',
		value='No Bonus: $1400\n```1 Loss: $1900```\n2 Losses: $2400\n3 Losses: $2900\nMax Loss: $3400', inline=True)
	await client.say(embed=embed)

async def loss2():
	await client.say('2 Round Loss Bonus - $2400')
	embed = discord.Embed(
		title=' ',
		color=discord.Color.orange()
	)
	embed.set_author(name='2 Loss Bonus')
	embed.add_field(
		name='Where we are',
		value='No Bonus: $1400\n1 Loss: $1900\n```2 Losses: $2400```\n3 Losses: $2900\nMax Loss: $3400', inline=True)
	await client.say(embed=embed)

async def loss3():
	await client.say('3 Round Loss Bonus - $2900')
	embed = discord.Embed(
		title=' ',
		color=discord.Color.red()
	)
	embed.set_author(name='3 Round Loss Bonus')
	embed.add_field(
		name='Where we are',
		value='No Bonus: $1400\n1 Loss: $1900\n2 Losses: $2400\n```3 Losses: $2900```\nMax Loss: $3400', inline=True)
	await client.say(embed=embed)

async def loss4():
	await client.say('Max Loss - $3400')
	embed = discord.Embed(
		title=' ',
		color=discord.Color.dark_red()
	)
	embed.set_author(name='MAX LOSS')
	embed.add_field(
		name='Where we are',
		value='No Bonus: $1400\n1 Loss: $1900\n2 Losses: $2400\n3 Losses: $2900\n```Max Loss: $3400```', inline=True)
	await client.say(embed=embed)

# Function that runs when !win or !loss is shouted that calls on Wally's responses above
async def winloss_status():
	global position
	if position == 0:
		await loss0()
	if position == 1:
		await loss1()
	if position == 2:
		await loss2()
	if position == 3:
		await loss3()
	if position >= 4:
		await loss4()

# Adds 1 round loss bonus every time someone shouts !loss
# Shows everyone what loss bonus they have by calling on Wally's responses
@client.command()
async def loss():
	global position
	if position < 4:
		position += 1
	await winloss_status()

# Removes 1 round loss bonus every time someone shouts !win
# Shows everyone what loss bonus they have by calling on Wally's responses
@client.command()
async def win():
	global position
	if position > 0:
		position -= 1
	await winloss_status()

# Responds with the current round loss bonus when someone shouts !status
@client.command()
async def status():
	await winloss_status()

# Resets to new half (each new half starts with a 1 round loss bonus)
@client.command()
async def new():
	global position
	position = 1
	await winloss_status()

# Manually sets loss bonus
@client.command()
async def set(number):
	global position
	error = 'Choose a round value (whole number) between 0 and 4'
	if number[0].isdigit() == False:
		await client.say(error)
	elif len(number) >= 2:
		await client.say(error)
	elif int(number[0]) <= 4 and int(number[0]) >= 0:
		position = int(number[0])
	else:
		await client.say(error)
	await winloss_status()

# Wally Help Message
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author

	embed = discord.Embed(
		color=discord.Color.orange()
	)

	embed.set_author(name="I track loss bonuses for CS:GO! Here are my commands:")
	embed.add_field(name="!win", value="Records a win to the counter", inline=False)
	embed.add_field(name="!loss", value="Records a loss to the counter", inline=False)
	embed.add_field(name="!status", value="Displays the current loss bonus", inline=False)
	embed.add_field(name="!new", value="Starts a new half with a loss bonus of 1", inline=False)
	embed.add_field(name="!set \"x\"", value="Manually set a loss bonus (0-4)", inline=False)

	await client.send_message(author, embed=embed)

client.run(TOKEN)
