from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter, ApplicationCommandMeta
from discord import Member, Message, User, Game, Embed, TextChannel, Role, RawReactionActionEvent, ApplicationCommandOption, ApplicationCommandOptionType

#* Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils



class thievery(Cog):
    def __init__(self, bot):
        self.bot = bot





def setup(bot):
    x = thievery(bot)
    bot.add_cog(x)