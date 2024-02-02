# Discord
from discord import Member

import utils

class GemFunction(object):
    bot = None



    @classmethod
    async def update_gems(cls, user:Member):
        c = utils.Currency.get(user.id)

        #! push coins to next tiers
        if c.silver >= 100:
            c.gold += 1
            c.silver -= 100

        if c.gold >= 100:
            c.emerald += 1
            c.gold -= 100

        if c.emerald >= 100:
            c.diamond += 1
            c.emerald -= 100

        if c.diamond >= 100:
            c.ruby += 1
            c.diamond -= 100

        if c.ruby >= 100:
            c.sapphire += 1
            c.ruby -= 100

        if c.sapphire >= 100:
            c.amethyst += 1
            c.sapphire -= 100

        if c.amethyst >= 100:
            c.phelstone += 1
            c.amethyst -= 100

        async with cls.bot.database() as db:
            await c.save(db)

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