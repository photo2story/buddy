import os
import discord
from discord.ext import commands
from bot import setup

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", intents=intents)

setup(bot)

@bot.event
async def on_ready():
    print(f'Bot has successfully logged in: {bot.user.name}')
    channel = bot.get_channel(int(os.getenv('DISCORD_CHANNEL_ID')))
    if channel:
        await channel.send(f'Bot has successfully logged in: {bot.user.name}')
    else:
        print(f"Cannot find the channel: {os.getenv('DISCORD_CHANNEL_ID')}")

# Discord 봇을 실행합니다.
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_APPLICATION_TOKEN'))
