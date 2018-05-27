import discord
import asyncio

client = discord.Client();

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged In")
	print(client.user.name)
	print(client.user.id)
	print('------')


