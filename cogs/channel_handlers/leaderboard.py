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

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild


        #+ Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(self.bot.config['leaderboard_messages']['1'])
        msg2 = await channel.fetch_message(self.bot.config['leaderboard_messages']['2'])

        #* Set up the embeds
        embed = Embed(color=randint(1, 0xffffff))
        embed2 = Embed(color=randint(1, 0xffffff))
        embed.description = "```fix\n█ Top 15 highest levels! █\n```\n"
        embed2.description = "```fix\n█ Top 30 highest levels! █\n```\n" 


        #* Add in level rankings
        sorted_rank = utils.Levels.sort_levels()
        ranks = sorted_rank[:30]
        users = []
        for i in sorted_rank:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 15:
                text.append(f"#{index+1} **{user.name}** --> Lvl.{floor(rank.level):,}")
            else:
                text2.append(f"#{index+1} **{user.name}** --> Lvl.{floor(rank.level):,}")

        embed.add_field(name='Level Rank', value='\n'.join(text), inline=True)
        embed2.add_field(name='Level Rank', value='\n'.join(text2), inline=True)

        await msg.edit(content=f"# Level Leaderboard", embed=embed)
        await msg2.edit(content=f" ", embed=embed2)




        #+ Coin Leaderboard
        msg = await channel.fetch_message(1095552313566965760)
        msg2 = await channel.fetch_message(1095552323557806260)

        #* Set up the embeds
        embed = Embed(color=randint(1, 0xffffff))
        embed2 = Embed(color=randint(1, 0xffffff))
        embed.description = "```fix\n█ Top 15 highest levels! █\n```\n"
        embed2.description = "```fix\n█ Top 30 highest levels! █\n```\n"


        sorted_rank = utils.Currency.sort_coins()
        ranks = sorted_rank[:22]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)

        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 10:
                text.append(f"#{index+1} **{user.name}** --> {self.bot.config['emotes']['coin']} {floor(rank.coins):,}")
            else:
                text2.append(f"#{index+1} **{user.name}** --> {self.bot.config['emotes']['coin']} {floor(rank.coins):,}")

        embed.add_field(name='Coin Rank', value='\n'.join(text), inline=True)
        embed2.add_field(name='Coin Rank', value='\n'.join(text2), inline=True)

        await msg.edit(content="**Those with the most coins!**", embed=embed)
        await msg2.edit(content=" ", embed=embed2)




    @five_minute_loop.before_loop
    async def before_five_minute_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""

        await self.bot.wait_until_ready()





def setup(bot):
    x = leaderboard(bot)
    bot.add_cog(x)