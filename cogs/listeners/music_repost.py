# Discord
from discord.ext.commands import Cog
from discord import RawReactionActionEvent, Embed

import utils

# Additions
from more_itertools import unique_everseen
from datetime import datetime as dt, timedelta
from asyncio import sleep
from math import floor

from re import search

class music_repost(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotifyReg = r"^https:\/\/open\.spotify\.com.*"



    @Cog.listener('on_message')
    async def music_handler_listener(self, message):
        """Looks for spotify music!"""

        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(1138195661288914995) #? music Channel

        #? Check for music channel
        if message.channel.id == ch.id:
            return

        if search(self.spotifyReg, message.content):
            await ch.send(f"**{message.author.name} Posted a song in <#{message.channel.id}>**\n {message.content}")





def setup(bot):
    x = music_repost(bot)
    bot.add_cog(x)