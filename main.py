import os
from flask import Flask
import discord
from discord.ext import commands
import threading

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
bot_instance = commands.Bot(command_prefix='', intents=intents)

@bot_instance.event
async def on_ready():
    print(f'Bot has successfully logged in: {bot_instance.user.name}')
    channel = bot_instance.get_channel(int(CHANNEL_ID))
    if channel:
        await channel.send(f'Bot has successfully logged in: {bot_instance.user.name}')
    else:
        print(f"Cannot find the channel: {CHANNEL_ID}")

if __name__ == "__main__":
    # bot.py의 명령어를 로드
    bot_instance.load_extension("bot")

    # Discord 봇 실행
    bot_thread = threading.Thread(target=lambda: bot_instance.run(TOKEN))
    bot_thread.start()

    # Flask 애플리케이션 실행
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
