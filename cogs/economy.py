import os
import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json

with open('./data.json') as f:
    d1 = json.load(f)

nest_asyncio.apply()

mongo_url = d1['mongo']

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
ecomoney = cluster["eco"]["money"]

class Economy(commands.Cog):
    """ Commands related to economy"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Eco Cog Loaded Succesfully")

    async def open_account(self, id : int):
        if id is not None:
            newuser = {"id": id, "wallet": 0, "bank": 100}
            # wallet = current money, bank = money in bank
            await ecomoney.insert_one(newuser)

    async def update_account(self, id : int, wallet : int, bank : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"wallet": wallet, "bank": bank}})


    @commands.command(aliases=["bal"])
    @cooldown(1, 2, BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        """ Check your balance"""
        if user is None:
            user = ctx.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                title=f"{user}'s Balance",
                color=0xFF0000,
            )
            embed.add_field(
                name="Wallet",
                value=f"${bal['wallet']}",
            )
            embed.add_field(
                name="Bank",
                value=f"${bal['bank']}",
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send('An error occured')

    @commands.command(aliases=["wd"])
    @cooldown(1, 2, BucketType.user)
    async def withdraw(self, ctx, amount: int):
        """ Withdraw money from your bank"""
        user = ctx.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            if amount > bal['bank']:
                await ctx.send('You do not have enough money to withdraw that much')
            elif amount <= 0:
                await ctx.send('You cannot withdraw 0 or less')
            else:
                await ecomoney.update_one({"id": user.id}, {"$inc": {"wallet": +amount, "bank": -amount}})
                await ctx.send(f'You have withdrawn ${amount}')
        except Exception:
            await ctx.send('An error occured')

    @commands.command(aliases=["dp"])
    @cooldown(1, 2, BucketType.user)
    async def deposit(self, ctx, amount: int):
        """ Deposit money to your bank"""
        user = ctx.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            if amount > bal['wallet']:
                await ctx.send('You do not have enough money to deposit that much')
            elif amount <= 0:
                await ctx.send('You cannot deposit 0 or less')
            else:
                await ecomoney.update_one({"id": user.id}, {"$inc": {"wallet": -amount, "bank": +amount}})
                await ctx.send(f'You have deposited ${amount}')
        except Exception:
            await ctx.send('An error occured')

def setup(bot):
    bot.add_cog(Economy(bot))