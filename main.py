from datetime import datetime, timedelta
from os import listdir, system

import aiohttp
import discord
import json

from discord.ext import commands
from pretty_help import PrettyHelp

system("clear")


class Echo(commands.Bot):
    def __init__(self):
        self.description = """Echo - A Economy Bot"""

        super().__init__(
            command_prefix={"."},
            owner_ids={727365670395838626},
            intents=discord.Intents.all(),
            help_command=PrettyHelp(),
            description=self.description,
            case_insensitive=True,
            start_time=datetime.utcnow(),
        )

    async def on_connnect(self):
        self.session = aiohttp.ClientSession(loop=self.loop)

        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Connected at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )

    async def on_ready(self):
        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Ready at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )
        print(f"[ Log ] GateWay WebSocket Latency: {self.latency*1000:.1f} ms")

with open('./data.json') as f:
  data = json.load(f)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        
TOKEN = data['token']
bot = Echo()

bot.load_extension("jishaku")
bot.loop.run_until_complete(bot.run(TOKEN))