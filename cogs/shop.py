import os
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import json

with open('./market.json') as f:
    d2 = json.load(f)

class Shop(commands.Cog):
    """ Commands related to market"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Shop Cog Loaded Succesfully")


    @commands.group(name="mkt", invoke_without_command=True)
    @cooldown(1, 2, BucketType.user)
    async def mkt(self,ctx):
        """ Market Commands"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Market Categories",
            color=0xFF0000,
        )
        embed.add_field(
            name="IoT",
            value="Buy items related to IoT/Technology | Use `.mkt iot`",
            inline=False
        )
        embed.add_field(
            name="Food",
            value="Buy items related to Food | Use `.mkt food`",
            inline=False
        )
        embed.add_field(
            name="Cars",
            value="Buy items related to Cars | Use `.mkt cars`",
            inline=False
        )
        embed.set_footer(
        text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )

        await ctx.send(embed=embed)

    @mkt.command(name="iot")
    @cooldown(1, 2, BucketType.user)
    async def iot(self,ctx):
        """ IoT/Technology Market"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="IoT Market",
            color=0xFF0000,
        )
        for x in d2["IoT"]:
            embed.add_field(
                name=x[0],
                value=f"Name {x[2]} | Price: ${x[1]}",
                inline=False
            )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    @mkt.command(name="food")
    @cooldown(1, 2, BucketType.user)
    async def food(self,ctx):
        """ Food Market"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Food Market",
            color=0xFF0000,
        )
        for x in d2["Food"]:
            embed.add_field(
                name=x[0],
                value=f"Name {x[2]} | Price: ${x[1]}",
                inline=False
            )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    @mkt.command(name="cars")
    @cooldown(1, 2, BucketType.user)
    async def cars(self,ctx):
        """ Cars Market"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Automobile Market",
            color=0xFF0000,
        )
        for x in d2["Cars"]:
            embed.add_field(
                name=x[0],
                value=f"Name {x[2]} | Price: ${x[1]}",
                inline=False
            )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Shop(bot))