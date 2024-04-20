from datetime import datetime, timedelta
from os import listdir
import os
import aiohttp
import discord
import json
from dotenv import load_dotenv

from discord.ext import commands

# Load environment variables from .env file
load_dotenv()

class Echo(commands.Bot):
    def __init__(self):
        self.description = """Echo - A Economy Bot"""

        super().__init__(
            command_prefix={"."},
            intents=discord.Intents.all(),
            description=self.description,
            case_insensitive=True,

        )

    async def on_connect(self):
        self.session = aiohttp.ClientSession(loop=self.loop)

        cT = datetime.now() + timedelta(hours=5, minutes=30)
        print(
            f"[ Log ] {self.user} Connected at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )

    async def on_ready(self):
        cT = datetime.now() + timedelta(hours=5, minutes=30)
        print(
            f"[ Log ] {self.user} Ready at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )
        print(f"[ Log ] GateWay WebSocket Latency: {self.latency*1000:.1f} ms")


with open("./market.json") as f:
    d2 = json.load(f)


def market_info():
    return d2


bot = Echo()

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Done")


@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Done")


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Done")


for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.load_extension("jishaku")
bot.loop.run_until_complete(bot.run(TOKEN))