from datetime import datetime
import pandas as pd
import numpy as np
from get_ticker import load_tickers, search_tickers, get_ticker_name, update_stock_market_csv
from estimate_stock import estimate_snp, estimate_stock
from Results_plot import plot_comparison_results, plot_results_all
from get_compare_stock_data import merge_csv_files, load_sector_info
from Results_plot_mpl import plot_results_mpl
import xml.etree.ElementTree as ET

from discord.ext import commands
from get_ticker import get_ticker_from_korean_name

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        print(f"Ping command received from {ctx.author.name}")
        await ctx.send(f'pong: {self.bot.user.name}')

    @commands.command(name="ticker")
    async def ticker(self, ctx, *, name):
        print(f"Ticker command received: {name}")
        ticker_symbol = get_ticker_from_korean_name(name)
        await ctx.send(f'Ticker symbol for {name} is {ticker_symbol}')

def setup(bot):
    bot.add_cog(BotCommands(bot))

# 이 코드는 디버깅 목적으로 추가합니다
if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="", intents=intents)
    setup(bot)
    TOKEN = os.getenv('DISCORD_APPLICATION_TOKEN')
    bot.run(TOKEN)



