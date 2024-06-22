# bot.py

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import certifi

# Load environment variables
load_dotenv()

# Discord bot token and channel ID from environment variables
TOKEN = os.getenv('DISCORD_APPLICATION_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# SSL certificate verification using certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot has successfully logged in: {bot.user.name}')
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        await channel.send(f'Bot has successfully logged in: {bot.user.name}')
    else:
        print(f"Cannot find the channel: {CHANNEL_ID}")

@bot.command()
async def ping(ctx):
    print(f"Ping command received from {ctx.author.name}")
    await ctx.send(f'pong: {bot.user.name}')

# Add other bot commands and functionalities as needed

bot.run(TOKEN)
