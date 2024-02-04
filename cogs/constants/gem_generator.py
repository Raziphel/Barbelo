
# Discord
from discord import Message
from discord.ext.commands import Cog
from discord.ext.tasks import loop
from more_itertools import unique_everseen

# Additions
from random import choice
from datetime import datetime as dt, timedelta
from re import compile

import utils

class Gem_Generator(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_gen_loop.start()
        self.valid_uri = compile(r"(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")


    @Cog.listener('on_message')
    async def Level_Progression(self, message:Message):
        '''Determine Level progression settings!'''

        #? Better not be in dms.
        if message.guild == None:
            return
        #? Better not be a bot.
        if message.author.bot:
            return
        #? Check if bot DB is connected!
        if self.bot.connected == False:
            return

        lvl = utils.Levels.get(message.author.id)
        g = utils.Gems.get(message.author.id)
        tr = utils.Tracking.get(member.id)


        if lvl.last_xp == None:
            lvl.last_xp = dt.utcnow()
        if (lvl.last_xp + timedelta(seconds=5)) <= dt.utcnow(): # Check Time

            #! Define varibles
            exp = 1
            unique_words = len(list(unique_everseen(message.content.split(), str.lower)))
            if message.attachments != None:
                unique_words += 6

            #! Unique Word Nerfer
            if unique_words > 10:
                unique_words = 8

            g.emerald += 1+unique_words
            exp += 1+unique_words

            await utils.UserFunction.level_up(user=message.author, channel=message.channel)

            #! Save it to database
            lvl.exp += exp+3
            lvl.last_xp = dt.utcnow()
            tr.messages += 1
        async with self.bot.database() as db:
            await lvl.save(db)
            await g.save(db)
            await tr.save(db)



    def cog_unload(self):
        self.exp_voice_gen.cancel()

    @loop(minutes=1)
    async def voice_gen_loop(self):
        #? Check if bot DB is connected!
        if self.bot.connected == False:
            return

        emeralds_payed = 0

        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:

                    tr = utils.Tracking.get(member.id)
                    tr.vc_mins += 1
                    async with self.bot.database() as db:
                        await tr.save(db)

                    #! Checks
                    checks = [
                        member.voice.deaf, 
                        member.voice.mute, 
                        member.voice.self_deaf, 
                        member.voice.afk,
                        member.bot,
                    ]
                    if any(checks):
                        break
                    if len(vc.members) < 2:
                        break

                    g = utils.Gems.get(member.id)
                    lvl = utils.Levels.get(member.id)
                    lvl.exp += 2 * (len(vc.members)/2)
                    g.emeralds = 25 * round(len(vc.members)/2)

                    await utils.UserFunction.level_up(user=member, channel=None)

                    async with self.bot.database() as db:
                        await g.save(db)
                        await lvl.save(db)
                        await tr.save(db)




    @voice_gen_loop.before_loop
    async def before_voice_gen_loop(self):
        await self.bot.wait_until_ready()



def setup(bot):
    x = Gem_Generator(bot)
    bot.add_cog(x)
