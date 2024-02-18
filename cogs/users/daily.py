
#* Discord
import discord
from discord.ext.commands import command, Cog, ApplicationCommandMeta, cooldown, BucketType

#* Additional
from random import choice
from datetime import datetime as dt, timedelta
from calendar import day_name

import utils




class daily(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #! The currency logs
    def gem_logs(self):
        return self.bot.get_channel(self.bot.config['logs']['gems'])



    @cooldown(1, 30, BucketType.user)
    @command(application_command_meta=ApplicationCommandMeta())
    async def daily(self, ctx):
        """Claim you daily rewards!"""
        #? Define variables
        day = utils.Daily.get(ctx.author.id)
        lvl = utils.Levels.get(ctx.author.id)
        g = utils.Gems.get(ctx.author.id)
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
                embed=utils.Embed(desc=f"⏰**You have already claimed your daily rewards!**\n       **You can claim them again in {t.hour} hours and {t.minute} minutes!**", color=tr.color)
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
        if daily > 90:
            daily = 90
        now = dt.now()
        emeralds = (10 + day.daily) * now.isoweekday()
        xps = lvl.level * now.isoweekday()

        g.emerald += emeralds
        lvl.exp += xps

        rewards = await utils.GemFunctions.gems_to_text(emeralds=emeralds)
        d = dt.today()
        x = day_name[d.weekday()]


        stringForm = str(day.daily) 
        lastDigit = stringForm[-1] 
        th = "th"
        if lastDigit == '1':
            th = "st"
        elif lastDigit == '2':
            th = "nd"
        elif lastDigit == '3':
            th = "rd"

        # ? Send the embed
        msg = await ctx.interaction.response.send_message(
            embed=utils.Embed(desc=f"# {ctx.author.name} Claimed their {x} Daily!\n**This is their {day.daily}{th} in a row!**\n**Rewards:**\n***{xps:,} XP***\n***{rewards}***", color=tr.color)
        )
        
        await self.gem_logs.send(f"{ctx.author.name} claimed daily!\nThis was their {day.daily}{th} in a row!\n**Rewards:**\n**{xps:,} ***XP***\n{rewards}")

        # * Save data changes
        async with self.bot.database() as db:
            await day.save(db)
            await lvl.save(db)
            await g.save(db)



def setup(bot):
    x = daily(bot)
    bot.add_cog(x)
