from quart import Quart, render_template, redirect, url_for, request
from quart_discord import DiscordOAuth2Session
import os
from dotenv import load_dotenv
import logging
from flask_cors import CORS

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Quart(__name__)
CORS(app)  # CORS 설정 추가

# 디버깅 정보 출력
app.logger.debug(f"DISCORD_CLIENT_ID: {os.getenv('DISCORD_CLIENT_ID')}")
app.logger.debug(f"DISCORD_CLIENT_SECRET: {os.getenv('DISCORD_CLIENT_SECRET')}")
app.logger.debug(f"DISCORD_REDIRECT_URI: {os.getenv('DISCORD_REDIRECT_URI')}")

app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET_KEY')
app.config["DISCORD_CLIENT_ID"] = os.getenv('DISCORD_CLIENT_ID')  # 디스코드 클라이언트 ID
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('DISCORD_CLIENT_SECRET')  # 디스코드 클라이언트 시크릿
app.config["DISCORD_REDIRECT_URI"] = os.getenv('DISCORD_REDIRECT_URI')  # 콜백 URL

discord = DiscordOAuth2Session(app)

@app.before_request
async def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', await request.get_data())

@app.after_request
async def log_response_info(response):
    app.logger.debug('Response status: %s', response.status)
    app.logger.debug('Response headers: %s', response.headers)
    return response

@app.route("/")
async def home():
    try:
        return await render_template("home.html", authorized=await discord.authorized)
    except Exception as e:
        app.logger.error(f"Error rendering home.html: {e}")
        return "Error rendering home.html", 500

@app.route("/login")
async def login():
    try:
        return await discord.create_session()
    except Exception as e:
        app.logger.error(f"Error during login: {e}")
        return "Error during login", 500

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception as e:
        app.logger.error(f"Error during callback: {e}")
        return "Error during callback", 500

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


# .\\.venv\\Scripts\\activate
# python main.py
