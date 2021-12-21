import discord
from discord.ext import commands

class Check(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Check Status Loaded Succesfully')

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong {ctx.author.mention}')



def setup(client):
    client.add_cog(Check(client))