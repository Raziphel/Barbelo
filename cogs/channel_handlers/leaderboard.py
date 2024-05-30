from math import floor
from asyncio import sleep
from datetime import datetime as dt, timedelta
from random import randint, choice

from discord import Game, Embed
from discord.ext import tasks
from discord.ext.commands import Cog

import utils


class leaderboard(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.five_minute_loop.start()



    @tasks.loop(minutes=5)
    async def five_minute_loop(self):
        """The loop that handles updating things every minute."""

        #! Database check
        if self.bot.connected == False:
            return

        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild


        #+ Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(self.bot.config['leaderboard_messages']['1'])
        msg2 = await channel.fetch_message(self.bot.config['leaderboard_messages']['2'])

        #* Set up the embeds
        embed = Embed(color=0xFFBF00)
        embed2 = Embed(color=0xFFBF00)

        #* Add in level rankings
        sorted_rank = utils.Levels.sort_levels()
        ranks = sorted_rank[:20]
        users = []
        for i in sorted_rank:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 10:
                text.append(f"#{index+1} **{user.name}** ─── Lvl.{floor(rank.level):,}")
            else:
                text2.append(f"#{index+1} **{user.name}** ─── Lvl.{floor(rank.level):,}")

        embed.description = '\n'.join(text)
        embed2.description = '\n'.join(text2)

        await msg.edit(content=f"# Level Leaderboard", embed=embed)
        await msg2.edit(content=f" ", embed=embed2)




        #+ Coin Leaderboard
        msg = await channel.fetch_message(self.bot.config['leaderboard_messages']['3'])
        msg2 = await channel.fetch_message(self.bot.config['leaderboard_messages']['4'])

        #* Set up the embeds
        embed = Embed(color=0x00ff00)
        embed2 = Embed(color=0x00ff00)


        sorted_rank = utils.Currency.sort_coins()
        ranks = sorted_rank[:20]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)

        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 10:
                text.append(f"#{index+1} **{user.name}** ─── {self.bot.config['emojis']['coin']}{floor(rank.coins):,}x")
            else:
                text2.append(f"#{index+1} **{user.name}** ─── {self.bot.config['emojis']['coin']}{floor(rank.coins):,}x")

        embed.description = '\n'.join(text)
        embed2.description = '\n'.join(text2)

        await msg.edit(content="# Coin Leaderboard", embed=embed)
        await msg2.edit(content=" ", embed=embed2)



        #+ Message Leaderboard
        msg = await channel.fetch_message(self.bot.config['leaderboard_messages']['5'])
        msg2 = await channel.fetch_message(self.bot.config['leaderboard_messages']['6'])

        #* Set up the embeds
        embed = Embed(color=0xFF0000)
        embed2 = Embed(color=0xFF0000)


        sorted_rank = utils.Tracking.sorted_messages()
        ranks = sorted_rank[:30]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)

        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 15:
                text.append(f"#{index+1} **{user.name}** ─── {rank.messages:,} msgs")
            else:
                text2.append(f"#{index+1} **{user.name}** ─── {rank.messages:,} msgs")

        embed.description = '\n'.join(text)
        embed2.description = '\n'.join(text2)

        await msg.edit(content="# Message Leaderboard", embed=embed)
        await msg2.edit(content=" ", embed=embed2)




        #+ VC MINS Leaderboard
        msg = await channel.fetch_message(self.bot.config['leaderboard_messages']['7'])
        msg2 = await channel.fetch_message(self.bot.config['leaderboard_messages']['8'])

        #* Set up the embeds
        embed = Embed(color=0x0000FF)
        embed2 = Embed(color=0x0000FF)


        sorted_rank = utils.Tracking.sorted_vc_mins()
        ranks = sorted_rank[:20]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)

        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 10:
                text.append(f"#{index+1} **{user.name}** ─── {floor(rank.vc_mins/60):,} hours")
            else:
                text2.append(f"#{index+1} **{user.name}** ─── {floor(rank.vc_mins/60):,} hours")

        embed.description = '\n'.join(text)
        embed2.description = '\n'.join(text2)

        await msg.edit(content="# VC Hour Leaderboard", embed=embed)
        await msg2.edit(content=" ", embed=embed2)



        #+ DAILY Leaderboard
        msg = await channel.fetch_message(self.bot.config['leaderboard_messages']['9'])
        msg2 = await channel.fetch_message(self.bot.config['leaderboard_messages']['10'])

        #* Set up the embeds
        embed = Embed(color=0xFF00FF)
        embed2 = Embed(color=0xFF00FF)


        sorted_rank = utils.Daily.sorted_daily()
        ranks = sorted_rank[:20]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)

        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 10:
                text.append(f"#{index+1} **{user.name}** ─── {rank.daily:,}th daily")
            else:
                text2.append(f"#{index+1} **{user.name}** ─── {rank.daily:,}th daily")

        embed.description = '\n'.join(text)
        embed2.description = '\n'.join(text2)

        await msg.edit(content="# Daily Leaderboard", embed=embed)
        await msg2.edit(content=" ", embed=embed2)






    @five_minute_loop.before_loop
    async def before_five_minute_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""

        await self.bot.wait_until_ready()





def setup(bot):
    x = leaderboard(bot)
    bot.add_cog(x)