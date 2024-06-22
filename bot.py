from datetime import datetime
import pandas as pd
import numpy as np
from get_ticker import load_tickers, search_tickers, get_ticker_name, update_stock_market_csv
from estimate_stock import estimate_snp, estimate_stock
from Results_plot import plot_comparison_results, plot_results_all
from get_compare_stock_data import merge_csv_files, load_sector_info
from Results_plot_mpl import plot_results_mpl
import xml.etree.ElementTree as ET
from get_ticker import get_ticker_from_korean_name

# Discord 설정
TOKEN = os.getenv('DISCORD_APPLICATION_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
# print(TOKEN)  # 이 줄을 추가하여 TOKEN 값을 출력
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
async def ticker(ctx, *, name):
    ticker_symbol = get_ticker_from_korean_name(name)
    await ctx.send(f'Ticker symbol for {name} is {ticker_symbol}')
    
@bot.command()
async def ping(ctx):
    print(f"Ping command received from {ctx.author.name}")
    await ctx.send(f'pong: {bot.user.name}')

tracemalloc.start()    

if __name__ == "__main__":
    bot.run(TOKEN)
