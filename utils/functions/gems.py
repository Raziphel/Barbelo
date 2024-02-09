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
        elif g.emerald < 0 and g.diamond > 0:
            g.emerald += 100
            g.diamond -= 1
        #? Diamond
        if g.diamond > 100:
            for x in range(floor(g.diamond/100)):
                g.diamond -= 100
                g.ruby += 1
        elif g.diamond < 0 and g.ruby > 0:
            g.diamond += 100
            g.ruby -= 1
        #? Ruby
        if g.ruby > 100:
            for x in range(floor(g.ruby/100)):
                g.ruby -= 100 
                g.sapphire += 1
        elif g.ruby < 0 and g.sapphire > 0:
            g.ruby += 100
            g.sapphire -= 1
        #? Sapphire
        if g.sapphire > 100:
            for x in range(floor(g.sapphire/100)):
                g.sapphire -= 100
                g.amethyst += 1
        elif g.sapphire < 0 and g.amethyst > 0:
            g.sapphire += 100
            g.amethyst -= 1
        #? Amethyst
        if g.amethyst > 100:
            for x in range(floor(g.amethyst/100)):
                g.amethyst -= 100
                g.hellstone += 1
        elif g.amethyst < 0 and g.hellstone > 0:
            g.amethyst += 100
            g.hellstone -= 1

        async with cls.bot.database() as db:
            await g.save(db)



    @classmethod
    async def payment(cls, user:Member, gem:str, amount:int):
        '''Pay for stuff with gems if they can afford it!  
        Returns false if it couldn't be purchased.'''

        g = utils.Gems.get(user.id)

        #? Hellstone
        if gem is "hellstone":
            if g.hellstone >= amount:
                g.hellstone -= amount
            else: return False
        #? Amethyst
        if gem is "amethyst":
            if g.amethyst >= amount:
                g.amethyst -= amount
            elif g.hellstone > 0:
                g.hellstone -= 1
                g.amethyst += 100
                g.amethyst -= amount
            else: return False
        #? Sapphire
        if gem is "sapphire":
            if g.sapphire >= amount:
                g.sapphire -= amount
            elif g.amethyst > 0:
                g.amethyst -= 1
                g.sapphire += 100
                g.sapphire -= amount
            else: return False
        #? Ruby
        if gem is "ruby":
            if g.ruby >= amount:
                g.ruby -= amount
            elif g.sapphire > 0:
                g.sapphire -= 1
                g.ruby += 100
                g.ruby -= amount
            else: return False
        #? Diamond
        if gem is "diamond":
            if g.diamond >= amount:
                g.diamond -= amount
            elif g.ruby > 0:
                g.ruby -= 1
                g.diamond += 100
                g.diamond -= amount
            else: return False
        #? Emerald
        if gem is "emerald":
            if g.emerald >= amount:
                g.emerald -= amount
            elif g.diamond > 0:
                g.diamond -= 1
                g.emerald += 100
                g.emerald -= amount
            else: return False

        async with cls.bot.database() as db:
            await g.save(db)



    @classmethod
    async def gems_to_text(cls, emeralds:int=0, diamonds:int=0, rubys:int=0, sapphires:int=0, amethysts:int=0, hellstones:int=0):
        '''Generates text showing how many gems you got.'''

        #? Emerald
        if emeralds > 100:
            for x in range(floor(emeralds/100)):
                emeralds -= 100
                diamonds += 1
        #? Diamond
        if diamonds > 100:
            for x in range(floor(diamonds/100)):
                diamonds -= 100
                rubys += 1
        #? Ruby
        if rubys > 100:
            for x in range(floor(rubys/100)):
                rubys -= 100 
                sapphires += 1
        #? Sapphire
        if sapphires > 100:
            for x in range(floor(sapphires/100)):
                sapphires -= 100
                amethysts += 1
        #? Amethyst
        if amethysts > 100:
            for x in range(floor(amethysts/100)):
                amethysts -= 100
                hellstones += 1

        flags = []
        if emeralds > 0:
            flags.append(f"{emeralds}x {cls.bot.config['gem_emoji']['emerald']}")
        if diamonds > 0:
            flags.append(f"{diamonds}x {cls.bot.config['gem_emoji']['diamond']}")
        if rubys > 0:
            flags.append(f"{rubys}x {cls.bot.config['gem_emoji']['ruby']}")
        if sapphires > 0:
            flags.append(f"{sapphires}x {cls.bot.config['gem_emoji']['sapphire']}")
        if amethysts > 0:
            flags.append(f"{amethysts}x {cls.bot.config['gem_emoji']['amethyst']}")
        if hellstones > 0:
            flags.append(f"{hellstones}x {cls.bot.config['gem_emoji']['hellstone']}")
        gems_string = ' '.join(flags)

        return gems_string
