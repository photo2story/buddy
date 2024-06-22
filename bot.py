import discord
from discord.ext import commands, ipc

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Server(self, secret_key="this_is_secret")

    async def on_ready(self):
        print("Bot is ready.")

    async def on_ipc_ready(self):
        print("IPC server is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

my_bot = MyBot(command_prefix="", intents=discord.Intents.default())

@my_bot.command()
async def ping(ctx):
    await ctx.send(f'pong: {my_bot.user.name}')

my_bot.ipc.start()
my_bot.run("YOUR_DISCORD_BOT_TOKEN")




