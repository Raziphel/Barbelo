# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel
# Utils
import utils


class CoinFunctions(object):
    bot = None


    @classmethod
    async def pay_user(cls, payer:Member, receiver:Member, amount:int):
        '''Use for payment between users (Taxed)'''

        #! Define Varibles
        cp = utils.Coins.get(payer.id)
        cr = utils.Coins.get(receiver.id)
        new_amount = await cls.pay_tax(payer=payer, amount=amount)
        taxed = amount - new_amount

        #! Check they have enough coins to pay.
        if cp.coins >= amount:

            #+ Give them coins and record
            cp.coins -= amount
            cp.gifted += amount

            cr.coins += amount
            cr.given += amount

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)
        return taxed #? Returns the amount taxed



    @classmethod 
    async def pay_tax(cls, payer:Member, amount:int):
        '''Use this method to pay the taxes for an amount then send the new amount back.'''

        #! Define Varibles
        cp = utils.Coins.get(payer.id)
        cr = utils.Coins.get(self.bot.config['bot_id'])

        #! Determine tax amount
        new_amount = amount*(0.92) #? 8% Tax
        taxed = amount - new_amount

        cp.coins -= taxed
        cp.taxed += taxed
        cr.coins += taxed

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)

        return new_amount



    @classmethod 
    async def pay_for(cls, payer:Member, amount:int):
        '''Use this method for purchases made!'''

        #! Define Varibles
        cp = utils.Coins.get(payer.id)
        cr = utils.Coins.get(self.bot.config['bot_id'])

        if cp.coins < amount:
            return false

        #+ Buy things with coins!
        cp.coins -= amount
        cp.spent += amount
        cr.coins += amount

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)

        return True



    @classmethod 
    async def earn(cls, earner:Member, amount:int):
        '''Use this method for letting users earn coins'''

        #! Define Varibles
        cu = utils.Coins.get(earner.id)
        cb = utils.Coins.get(self.bot.config['bot_id'])

        #! Check if the bank's got coins!
        if cb.coins <= 10000:
            
            return

        #+ Just take it away from the bot!
        cu.coins += amount
        cu.earned += amount
        cb.coins -= amount

        async with cls.bot.database() as db:
            await cu.save(db)
            await cb.save(db)
