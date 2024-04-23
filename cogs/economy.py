import os
import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json
import random

nest_asyncio.apply()

with open('./data.json') as f:
    config = json.load(f)

cluster = motor.motor_asyncio.AsyncIOMotorClient(config["mongo"])
economy_collection = cluster["eco"]["money"]


class Economy(commands.Cog):
    """Commands related to economy"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy cog loaded successfully")

    async def create_account(self, user_id):
        new_account = {"id": user_id, "wallet": 0, "bank": 100}
        await economy_collection.insert_one(new_account)

    async def update_wallet(self, user_id, amount):
        await economy_collection.update_one(
            {"id": user_id}, {"$set": {"wallet": amount}}
        )

    async def update_bank(self, user_id, amount):
        await economy_collection.update_one(
            {"id": user_id}, {"$set": {"bank": amount}}
        )

    @commands.command(aliases=["bal"])
    @cooldown(1, 2, BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        """Check your balance"""
        if user is None:
            user = ctx.author
        account = await economy_collection.find_one({"id": user.id})
        if account is None:
            await self.create_account(user.id)
            account = await economy_collection.find_one({"id": user.id})
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title=f"{user}'s Balance",
            color=0xFF0000,
        )
        embed.add_field(name="Wallet", value=f"${account['wallet']}")
        embed.add_field(name="Bank", value=f"${account['bank']}")
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}"
        )
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["wd"])
    @cooldown(1, 10, BucketType.user)
    async def withdraw(self, ctx, amount: int):
        """Withdraw money from your bank"""
        account = await economy_collection.find_one({"id": ctx.author.id})
        if account is None:
            await self.create_account(ctx.author.id)
            account = await economy_collection.find_one({"id": ctx.author.id})
        if amount > account["bank"]:
            await ctx.send("You do not have enough money to withdraw that much")
        elif amount <= 0:
            await ctx.send("You cannot withdraw 0 or less")
        else:
            await self.update_wallet(ctx.author.id, account["wallet"] + amount)
            await self.update_bank(ctx.author.id, account["bank"] - amount)
            await ctx.send(f"You have withdrawn ${amount}")

    @commands.command(aliases=["dp"])
    @cooldown(1, 10, BucketType.user)
    async def deposit(self, ctx, amount: int):
        """Deposit money to your bank"""
        account = await economy_collection.find_one({"id": ctx.author.id})
        if account is None:
            await self.create_account(ctx.author.id)
            account = await economy_collection.find_one({"id": ctx.author.id})
        if amount > account["wallet"]:
            await ctx.send("You do not have enough money to deposit that much")
        elif amount <= 0:
            await ctx.send("You cannot deposit 0 or less")
        else:
            await self.update_wallet(ctx.author.id, account["wallet"] - amount)
            await self.update_bank(ctx.author.id, account["bank"] + amount)
            await ctx.send(f"You have deposited ${amount}")

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def rob(self, ctx, user: discord.Member = None):
        """Rob someone"""
        if user is None or user.id == ctx.author.id:
            await ctx.send("Trying to rob yourself?")
        else:
            victim_account = await economy_collection.find_one({"id": user.id})
            if victim_account is None:
                await self.create_account(user.id)
                victim_account = await economy_collection.find_one({"id": user.id})
            robbers_account = await economy_collection.find_one({"id": ctx.author.id})
            if robbers_account is None:
                await self.create_account(ctx.author.id)
                robbers_account = await economy_collection.find_one({"id": ctx.author.id})
            robber_bank = robbers_account["bank"]
            victim_bank = victim_account["bank"]
            if robber_bank < 100:
                await ctx.send("You do not have enough money to rob someone")
            elif robber_bank >= 100:
                if victim_bank < 100:
                    await ctx.send("User do not have enough money to get robbed ;-;")
                elif victim_bank >= 100:
                    amount = random.randint(1, 100)
                    robbers_account["bank"] += amount
                    victim_account["bank"] -= amount
                    await economy_collection.update_one(
                        {"id": ctx.author.id}, {"$set": robbers_account}
                    )
                    await economy_collection.update_one(
                        {"id": user.id}, {"$set": victim_account}
                    )
                    await ctx.send(f"You have robbed ${amount} from {user}")

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def send(self, ctx, user: discord.Member, amount: int):
        """Send money to another user"""
        receiver_account = await economy_collection.find_one({"id": user.id})
        sender_account = await economy_collection.find_one({"id": ctx.author.id})
        if receiver_account is None:
            await self.create_account(user.id)
            receiver_account = await economy_collection.find_one({"id": user.id})
        if sender_account is None:
            await self.create_account(ctx.author.id)
            sender_account = await economy_collection.find_one({"id": ctx.author.id})
        sender_bank = sender_account["bank"]
        receiver_bank = receiver_account["bank"]
        if amount > sender_bank or amount > 20000:
            await ctx.send("You do not have enough money to send that much")
        elif amount <= 0:
            await ctx.send("You cannot send 0 or less")
        else:
            sender_account["bank"] -= amount
            receiver_account["bank"] += amount
            await economy_collection.update_one(
                {"id": ctx.author.id}, {"$set": sender_account}
            )
            await economy_collection.update_one(
                {"id": user.id}, {"$set": receiver_account}
            )
            await ctx.send(f"You have sent ${amount} to {user}")

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def beg(self, ctx):
        """ Beg for some money from strangers """
        beg_amount = random.randint(0, 500)
        user_bal = await economy_collection.find_one({"id": ctx.author.id})
        if not user_bal:
            await self.open_account(ctx.author.id)
            user_bal = await economy_collection.find_one({"id": ctx.author.id})
        await economy_collection.update_one({"id": ctx.author.id}, {"$inc": {"wallet": +beg_amount}})
        reactions = ['💸', '🤑', '💰', '💳', '💵']
        excuses = ["You're lucky I have a heart of gold!",
                   "Don't beg, just take what you want.",
                   "I'm not as poor as you think I am.",
                   "I'm feeling generous today, so here you go!",
                   "You're welcome."]
        excuse = random.choice(excuses)
        embed = discord.Embed(title=random.choice(reactions), description = f"{ctx.author.mention} {excuse} ${beg_amount}")
        embed.color = discord.Color.gold()
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def gamble(self, ctx, amount: int):
        """Gamble some money."""
        try:
            user_bal = await economy_collection.find_one({"id": ctx.author.id})
            if user_bal is None:
                await self.open_account(ctx.author.id)
                user_bal = await economy_collection.find_one({"id": ctx.author.id})
            if amount > user_bal["wallet"]:
                await ctx.send("You do not have enough money to gamble that much.")
            elif amount <= 0:
                await ctx.send("You cannot gamble 0 or less.")
            else:
                num = random.randint(1, 100)
                if num <= 50:
                    await economy_collection.update_one({"id": ctx.author.id}, {"$inc": {"wallet": amount}})
                    embed = discord.Embed(title="You won!", description=f"You won ${amount}!", color=discord.Color.green())
                else:
                    await economy_collection.update_one({"id": ctx.author.id}, {"$inc": {"wallet": -amount}})
                    embed = discord.Embed(title="You lost!", description=f"You lost ${amount}!", color=discord.Color.red())
                await ctx.send(embed=embed)
        except Exception:
            await ctx.send("An error occurred.")
   
def setup(bot):
    bot.add_cog(Economy(bot))
