# Discord
from discord import Member

from math import floor

import utils

class GemFunctions(object):
    bot = None



    @classmethod
    async def update(cls, user:Member):
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
    async def downgrade(cls, user:Member):
        g = utils.Gems.get(user.id)

        #+ Lower every gem by one to check if they can afford
        if g.hellstone > 0:
            g.hellstone -= 1
            g.amethyst += 100

        if g.amethyst > 0:
            g.amethyst -= 1
            g.sappire += 100

        if g.sapphire > 0:
            g.sapphire -= 1
            g.ruby += 100

        if g.ruby > 0:
            g.ruby -= 1
            g.diamond += 100

        if g.diamond > 0:
            g.diamond -= 1
            g.emerald += 100

        if g.emerald > 0:
            g.emerald -= 1
            g.gold += 100

        async with cls.bot.database() as db:
            await g.save(db)