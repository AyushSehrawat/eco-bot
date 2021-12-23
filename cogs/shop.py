import os
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json

with open('./data.json') as f:
    d1 = json.load(f)
with open('./market.json') as f:
    d2 = json.load(f)

items = {}

for x in d2["IoT"]:
    i = {x[2] : ["iot", x[1], x[0]]}    
    items.update(i)

for x in d2["Food"]:
    i = {x[2] : ["food", x[1], x[0]]}
    items.update(i)

for x in d2["Cars"]:
    i = {x[2] : ["cars", x[1], x[0]]}
    items.update(i)

#print(items)

nest_asyncio.apply()

mongo_url = d1['mongo']

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
ecomoney = cluster["eco"]["money"]
ecobag = cluster["eco"]["bag"]

class Shop(commands.Cog):
    """ Commands related to market"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Shop Cog Loaded Succesfully")


    async def open_account(self, id : int):
        if id is not None:
            newuser = {"id": id, "wallet": 0, "bank": 100}
            # wallet = current money, bank = money in bank
            await ecomoney.insert_one(newuser)

    async def update_wallet(self, id : int, wallet : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"wallet": wallet}})

    async def update_bank(self, id : int, bank : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"bank": bank}})

    async def open_bag(self, id : int):
        if id is not None:
            newuser = {"id": id, "bag": []}
            await ecobag.insert_one(newuser)


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

    # ---------------------------- In Progress

    @commands.command(aliases=["b"])
    @cooldown(1, 2, BucketType.user)
    async def buy(self, ctx, item : str, amount : int = 1):
        if amount <= 0:
            await ctx.send("Amount must be greater than 0")
            return
        bal = await ecomoney.find_one({"id": ctx.author.id})
        if bal is None:
            await self.open_account(ctx.author.id)
            bal = await ecomoney.find_one({"id": ctx.author.id})

        bag = await ecobag.find_one({"id": ctx.author.id})
        if bag is None:
            await self.open_bag(ctx.author.id)
            bag = await ecobag.find_one({"id": ctx.author.id})
        
        fg = items.get(item)

        if fg is None:
            await ctx.send("Item not found")
            return

        price = fg[1] * amount
        name = fg[2]

        u_bal = bal["bank"]

        if u_bal < price:
            await ctx.send("You don't have enough money in your bank")
            return

        await ctx.send(bag['bag'])


        am = amount
        for x in bag['bag']:
            if x[item]:
                inde = bag['bag'].index(x)
                am = bag['bag'][inde][item]
                am += amount

        # Update amount or add in bag
        print(am)
        if am > amount:
            await ecobag.update_one({"id": ctx.author.id}, {"$set": {"bag.$.{}".format(item): am}})

        else:
            await ecobag.update_one({"id": ctx.author.id}, {"$push": {"bag": {"{}".format(item): amount}}})

        # await ecobag.update_one({"id": ctx.author.id}, {"$set": {"bag.$.{}".format(item): am}})
        await ctx.send(f"{ctx.author.mention} bought {amount} {name} for ${price}")

        f_u_bal = u_bal - price
        await self.update_bank(ctx.author.id, f_u_bal)

        
        

def setup(bot):
    bot.add_cog(Shop(bot))