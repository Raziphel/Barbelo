
#* Discord
from discord import RawReactionActionEvent, Embed, PartialEmoji, Message, Member, DiscordException, guild
from discord.ext.commands import Cog

# * Additions
from asyncio import sleep, TimeoutError
from math import floor
from random import randint
from typing import Optional
from re import findall

import utils


class VerificationCancelled(BaseException):
    pass


def get_only_numbers(data: str):
    try:
        numbers_list = findall(r'\d+', data)
        numbers = ''.join(numbers_list)

        return int(numbers)
    except ValueError:
        return None



class purgatory(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #+ The Server Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 



    @Cog.listener('on_ready') #! ---> Server Rules
    async def rules(self):

        embed1=Embed(description=f"# __**Welcome to Esoterica**__\nEsoterica is not meant to be a normal Discord server thats sole purpose is for socializing and posting memes with your friends.\n\nHere in esoterica, members of the server are all given roles and abilities that make them capable of doing almost anything...\n\n**All members are required to accept the Esoterica - Terms of Service.**", color=0xff0000)

        embed2=Embed(description=f"# __**Terms of Service**__\nBy choosing to be apart of Esoterica, you understand that you may be subject to \"unfair treatment\" and \"punishments\" that are automated and not brought on by any members of staff.\n\n", color=0x000000)

        embed3=Embed(description=f"", color=0xff0000)

        embed4=Embed(description=f"", color=0xBEBEBE)


        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['welcome']) 

        welcome_banner = await ch.fetch_message(self.bot.config['welcome_messages']['banner_id']) #? 
        await welcome_banner.edit(content=f"{self.bot.config['welcome_messages']['banner_url']}")

        tos_banner = await ch.fetch_message(self.bot.config['welcome_messages']['tos_id']) #? 
        await tos_banner.edit(content=f"{self.bot.config['welcome_messages']['tos_url']}")

        rules = {}
        for i in range(1, 3):
            rules[i] = await ch.fetch_message(self.bot.config['welcome_messages'][str(i)])

        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9]

        for i, rule in rules.items():
            await rule.edit(content="", embed=embeds[i-1])





def setup(bot):
    x = purgatory(bot)
    bot.add_cog(x)