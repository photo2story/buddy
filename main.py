from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # this is required because OAuth 2 utilizes https.

app = Quart(__name__)

app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # You should set this to a secure random value
app.config["DISCORD_CLIENT_ID"] = os.getenv('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('DISCORD_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = os.getenv('DISCORD_REDIRECT_URI')

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
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run()
