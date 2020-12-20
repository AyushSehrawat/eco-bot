import discord
from discord.ext import commands
import psutil


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()

    async def on_ready(self):
        print('Info Cog Loaded Succesfully')

    @commands.command(aliases=['python', 'botinfo'])
    async def bot(self, ctx):
        values = psutil.virtual_memory()
        val2 = values.available * 0.001
        val3 = val2 * 0.001
        val4 = val3 * 0.001

        values2 = psutil.virtual_memory()
        value21 = values2.total
        values22 = value21 * 0.001
        values23 = values22 * 0.001
        values24 = values23 * 0.001

        embedve = discord.Embed(
            title="Bot Info", description=None, color=0x9370DB)
        embedve.add_field(
            name="Bot Latency", value=f"Bot latency - {round(self.client.latency * 1000)}ms", inline=False)
        embedve.add_field(name='Hosting Stats', value=f'Cpu usage- {psutil.cpu_percent(1)}%'
                          f'\n(Actual Cpu Usage May Differ)'
                          f'\n'

                          f'\nNumber OF Cores - {psutil.cpu_count()} '
                          f'\nNumber of Physical Cores- {psutil.cpu_count(logical=False)}'
                          f'\n'

                          f'\nTotal ram- {round(values24, 2)} GB'
                          f'\nAvailable Ram - {round(val4, 2)} GB')

        await ctx.send(embed=embedve)

    @commands.command(aliases=['help'])
    async def _help(self, ctx):
        embedvar = discord.Embed(title="Help Commands",description=None, color=0x00ff00)

        embedvar.add_field(name=')bot', value='To see bot info', inline=False)
        embedvar.add_field(name=')balance / )bal', value='To see your balance', inline=False)
        embedvar.add_field(name=')beg', value='To beg some money', inline=False)
        embedvar.add_field(name=')deposit', value='To deposit money in bank', inline=False)
        embedvar.add_field(name=')withdraw', value='To withdraw money from bank', inline=False)
        embedvar.add_field(name=')send', value='Send money to someone', inline=False)
        embedvar.add_field(name=')rob', value='Rob some random money ', inline=False)
        embedvar.add_field(name=')slots', value='To bet some money', inline=False)
        embedvar.add_field(name=')shop', value='To view shop', inline=False)
        embedvar.add_field(name=')buy', value='To, buy an item', inline=False)
        embedvar.add_field(name=')sell', value='To sell an item', inline=False)
        embedvar.add_field(name=')bag', value='To view your shopping cart', inline=False)
        embedvar.add_field(name=')lb', value='To view leaderboard', inline=False)

        await ctx.send(embed=embedvar)

def setup(client):
    client.add_cog(Info(client))
