from flask import Flask, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
import discord
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Buddy Plotter!"})

@app.route('/api/stock', methods=['GET'])
def get_stock():
    return jsonify({"stock": "AAPL", "price": 150})

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.before_request
def before_request():
    app.logger.debug("Request started")

@app.after_request
def after_request(response):
    app.logger.debug("Request finished")
    return response

def run_flask():
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

def run_discord_bot():
    bot.run(TOKEN)

if __name__ == '__main__':
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Discord bot
    run_discord_bot()
