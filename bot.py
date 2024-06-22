import os
import discord
from discord.ext import commands
from get_ticker import get_ticker_from_korean_name

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot has successfully logged in: {bot.user}')

@bot.command()
async def ticker(ctx, *, name):
    ticker_symbol = get_ticker_from_korean_name(name)
    await ctx.send(f'Ticker symbol for {name} is {ticker_symbol}')

if __name__ == "__main__":
    bot.run(TOKEN)
