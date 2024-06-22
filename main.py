import os
from flask import Flask
import discord
from discord.ext import commands
from get_ticker import get_ticker_from_korean_name

# Flask 애플리케이션 설정
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Heroku!"

# Discord 설정
TOKEN = os.getenv('DISCORD_APPLICATION_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot has successfully logged in: {bot.user.name}')
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        await channel.send(f'Bot has successfully logged in: {bot.user.name}')
    else:
        print(f"Cannot find the channel: {CHANNEL_ID}")

@bot.command()
async def ticker(ctx, *, name):
    ticker_symbol = get_ticker_from_korean_name(name)
    await ctx.send(f'Ticker symbol for {name} is {ticker_symbol}')

@bot.command()
async def ping(ctx):
    print(f"Ping command received from {ctx.author.name}")
    await ctx.send(f'pong: {bot.user.name}')

if __name__ == "__main__":
    # Discord 봇 실행
    import threading
    bot_thread = threading.Thread(target=lambda: bot.run(TOKEN))
    bot_thread.start()

    # Flask 애플리케이션 실행
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
