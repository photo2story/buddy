from datetime import datetime
import pandas as pd
import numpy as np
from get_ticker import load_tickers, search_tickers, get_ticker_name, update_stock_market_csv
from estimate_stock import estimate_snp, estimate_stock
from Results_plot import plot_comparison_results, plot_results_all
from get_compare_stock_data import merge_csv_files, load_sector_info
from Results_plot_mpl import plot_results_mpl
import xml.etree.ElementTree as ET

import os
import discord
from discord.ext import commands
from get_ticker import get_ticker_from_korean_name

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        print(f"Ping command received from {ctx.author.name}")
        await ctx.send(f'pong: {self.bot.user.name}')

    @commands.command()
    async def ticker(self, ctx, *, name):
        print(f"Ticker command received: {name}")
        ticker_symbol = get_ticker_from_korean_name(name)
        await ctx.send(f'Ticker symbol for {name} is {ticker_symbol}')

def setup(bot):
    bot.add_cog(BotCommands(bot))


