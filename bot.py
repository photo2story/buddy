import discord
from discord.ext import commands
import os

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")
        print(f"Ping command received from {ctx.author.name}")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Bot has successfully logged in: {bot.user.name}")

bot.add_cog(BotCommands(bot))

bot.run(os.getenv('DISCORD_TOKEN'))
