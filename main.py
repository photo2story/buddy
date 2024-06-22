from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Discord Bot
TOKEN = os.getenv('DISCORD_APPLICATION_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        await channel.send(f'Bot has successfully logged in: {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)
