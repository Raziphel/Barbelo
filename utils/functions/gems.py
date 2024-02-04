# Discord
from discord import Member

from math import floor

import utils

class GemFunctions(object):
    bot = None



    @classmethod
    async def update(cls, user:Member):
        '''Simply updates gems to the next tier'''

        g = utils.Gems.get(user.id)

        #? Emerald
        if g.emerald > 100:
            for x in range(floor(g.emerald/100)):
                g.emerald -= 100
                g.diamond += 1
        #? Diamond
        if g.diamond > 100:
            for x in range(floor(g.diamond/100)):
                g.diamond -= 100
                g.ruby += 1
        #? Ruby
        if g.ruby > 100:
            for x in range(floor(g.ruby/100)):
                g.ruby -= 100 
                g.sapphire += 1
        #? Sapphire
        if g.sapphire > 100:
            for x in range(floor(g.sapphire/100)):
                g.sapphire -= 100
                g.amethyst += 1
        #? Amethyst
        if g.amethyst > 100:
            for x in range(floor(g.amethyst/100)):
                g.amethyst -= 100
                g.hellstone += 1
        async with cls.bot.database() as db:
            await g.save(db)



    @classmethod
    async def payment(cls, user:Member, gem:str):
        '''Pay for stuff with gems if they can afford it!  
        Returns true if it was purchased.'''

        g = utils.Gems.get(user.id)

        #+ Lower every gem by one to check if they can afford
        #? Hellstone
        if g.hellstone > 0:
            g.hellstone -= 1
            g.amethyst += 100
        #? Amethyst
        if g.amethyst > 0:
            g.amethyst -= 1
            g.sappire += 100
        #? Sapphire
        if g.sapphire > 0:
            g.sapphire -= 1
            g.ruby += 100
        #? Ruby
        if g.ruby > 0:
            g.ruby -= 1
            g.diamond += 100
        #? Diamond
        if g.diamond > 0:
            g.diamond -= 1
            g.emerald += 100
        #? Emerald
        if g.emerald > 0:
            g.emerald -= 1
            g.gold += 100
        async with cls.bot.database() as db:
            await g.save(db)