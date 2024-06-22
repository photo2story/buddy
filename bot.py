# bot.py

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import certifi

# Load environment variables
load_dotenv()

# Discord bot token and channel ID from environment variables
TOKEN = os.getenv('DISCORD_APPLICATION_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# SSL certificate verification using certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

intents = discord.Intents.all()
intents.message_content = True
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

# 여기에 필요한 다른 봇 명령어와 기능 추가

bot.run(TOKEN)
