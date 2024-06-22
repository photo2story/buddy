from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session
import os
import asyncio
import subprocess

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # This is required because OAuth 2 utilizes https.

app = Quart(__name__)

app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')
app.config["DISCORD_CLIENT_ID"] = os.getenv('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('DISCORD_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = os.getenv('DISCORD_REDIRECT_URI')

# Debug output for environment variables
print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
print(f"DISCORD_CLIENT_ID: {app.config['DISCORD_CLIENT_ID']}")
print(f"DISCORD_CLIENT_SECRET: {app.config['DISCORD_CLIENT_SECRET']}")
print(f"DISCORD_REDIRECT_URI: {app.config['DISCORD_REDIRECT_URI']}")

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    return await render_template("home.html", authorized=await discord.authorized)

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Run the bot in a separate process
    bot_process = subprocess.Popen(["python", "bot.py"])
    
    # Get the port from the environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Run the Quart app
    app.run(port=port)
