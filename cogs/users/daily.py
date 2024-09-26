#* Discord
import discord
from discord.ext.commands import command, Cog, ApplicationCommandMeta, cooldown, BucketType

#* Additional
from random import choice
from datetime import datetime as dt, timedelta
from calendar import day_name
from math import floor

import utils


class daily(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #! The currency logs
    def coin_logs(self):
        return self.bot.get_channel(self.bot.config['logs']['coins'])

    @cooldown(1, 30, BucketType.user)
    @command(application_command_meta=ApplicationCommandMeta())
    async def daily(self, ctx):
        """Claim you daily rewards!"""
        #? Define variables
        day = utils.Daily.get(ctx.author.id)
        lvl = utils.Levels.get(ctx.author.id)
        c = utils.Currency.get(ctx.author.id)
        tr = utils.Tracking.get(ctx.author.id)

        #? Check if it's first daily
        if not day.daily:
            day.daily = 1
            day.last_daily = (dt.utcnow() - timedelta(days=3))

        #? Check if already claimed
        if (day.last_daily + timedelta(hours=22)) >= dt.utcnow():
            tf = day.last_daily + timedelta(hours=22)
            t = dt(1, 1, 1) + (tf - dt.utcnow())
            return await ctx.interaction.response.send_message(
                embed=utils.Embed(
                    desc=f"⏰**You have already claimed your daily rewards!**\n**You can claim them again in {t.hour} hours and {t.minute} minutes!**",
                    user=ctx.author)
            )

        #? Missed daily
        elif (day.last_daily + timedelta(days=3)) <= dt.utcnow():
            day.daily = 1
            day.last_daily = dt.utcnow()

        #? Got daily
        elif (day.last_daily + timedelta(hours=22)) <= dt.utcnow():
            day.daily += 1
            day.last_daily = dt.utcnow()

            #! Determine rewards
        daily = day.daily
        if daily > 350:
            daily = 350
        now = dt.now()
        coins = 2.5 * ((10 + day.daily) * now.isoweekday())

        await utils.CoinFunctions.earn(earner=ctx.author, amount=coins)

        d = dt.today()
        x = day_name[d.weekday()]

        stringForm = str(day.daily)
        lastDigit = stringForm[-1]
        th = "th"
        if day.daily > 3:
            th = "th"
        elif lastDigit == '1':
            th = "st"
        elif lastDigit == '2':
            th = "nd"
        elif lastDigit == '3':
            th = "rd"

        # ? Send the embed
        msg = await ctx.interaction.response.send_message(
            embed=utils.Embed(
                desc=f"# This is your {day.daily}{th} daily claimed in a row!\n```\nYou have been rewarded:\n```\n***{self.bot.config['emojis']['coin']}{floor(coins):,}x***",
                user=ctx.author)
        )

        await self.coin_logs.send(
            f"***{ctx.author.name} claimed there your {day.daily}{th} daily claimed in a row!***\n```\nYou have been rewarded:\n```\n***{self.bot.config['emojis']['coin']}{floor(coins):,}x***")

        # * Save data changes
        async with self.bot.database() as db:
            await day.save(db)
            await lvl.save(db)
            await c.save(db)


def setup(bot):
    x = daily(bot)
    bot.add_cog(x)
