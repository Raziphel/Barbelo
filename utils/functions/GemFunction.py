# Discord
from discord import Member

from math import floor

import utils

class GemFunctions(object):
    bot = None



    @classmethod
    async def update_gems(cls, user:Member):
        g = utils.Gems.get(user.id)

        #+ Upgrade gems to the next tier!

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

        return




    @classmethod
    async def pay_exchange(cls, user:Member):
        c = utils.Currency.get(user.id)

        #! Lower every gem by one to check if they can afford
        if c.phelstone > 0:
            c.phelstone -= 1
            c.amethyst += 100

        if c.amethyst > 0:
            c.amethyst -= 1
            c.sappire += 100

        if c.sapphire > 0:
            c.sapphire -= 1
            c.ruby += 100

        if c.ruby > 0:
            c.ruby -= 1
            c.diamond += 100

        if c.diamond > 0:
            c.diamond -= 1
            c.emerald += 100

        if c.emerald > 0:
            c.emerald -= 1
            c.gold += 100

        if c.gold > 0:
            c.gold -= 1
            c.silver += 100

        async with cls.bot.database() as db:
            await c.save(db)