# Discord
# Additions
from asyncio import sleep
from random import choice, randint

from discord import RawReactionActionEvent
from discord.ext.commands import Cog

import utils


class Message_Rewards(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bunny_messages = []
        self.coin_messages = []
        self.sparkle_messages = []
        self.bun_msg = 0


    @Cog.listener('on_message')
    async def reward_gen(self, message):
        """Message Reward Generation"""

        #? BETTER NOT BE A DM
        if message.guild is None:
            return
        #? Disables Bots
        if message.author.bot:
            return
        #? Check if bot is connected!
        if not self.bot.connected:
            return

        #! Define some variables
        user = message.author
        messages = await message.channel.history(limit=10).flatten()

        #! Give them some rewards!
        try:
            chance = randint(1, 25000)
            if chance <= 25:
                message = choice(messages)
                await message.add_reaction("✨")
                self.sparkle_messages.append(message.id)
            elif chance <= 75:
                for x in range(5):
                    message = choice(messages)
                    reaction = await message.add_reaction(self.bot.config['emojis']['bunny'])
                    self.bunny_messages.append(message.id)
            elif chance <= 500:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emojis']['coin'])
                self.coin_messages.append(message.id)
        except Exception as e:
            print(f'A reward failed to spawn :: {e}')

        await sleep(10)




    @Cog.listener('on_raw_reaction_add')
    async def item_reaction_handler(self, payload:RawReactionActionEvent):
        """Handles reactions with the items"""

        #? Check if bot is connected!
        if not self.bot.connected:
            return


        #? BETTER NOT BE A DM
        guild = self.bot.get_guild(payload.guild_id)
        user = self.bot.get_user(payload.user_id)
        if guild is None:
            return

        #? Check not a bot
        if user.bot:
            return

        #! Define Variables
        channel = guild.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
        except: return
        msg = None

        c = utils.Currency.get(user.id)
        coin_logs = self.bot.get_channel(self.bot.config['logs']['coins'])

        #! Define Emojis
        bunny_e = self.bot.config['emojis']['bunny']
        coin_e = self.bot.config['emojis']['coin']

        #! Get the correct item
        if str(payload.emoji) == coin_e:
            if message.id in self.coin_messages:
                self.coin_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([300, 450, 500, 650, 700, 750])
                await utils.CoinFunctions.earn(earner=user, amount=coin)
                msg = await channel.send(f"{user.name} found **{coin} {coin_e}x**")
                await coin_logs.send(f"**{user}** found **{coin} {coin_e}**")

        elif str(payload.emoji) == bunny_e:
            if message.id in self.bunny_messages:
                self.bunny_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([500, 750, 1000])
                await utils.CoinFunctions.earn(earner=user, amount=coin)
                msg = await channel.send(f"{user.name} got **{coin} {coin_e}x from a bunny!**")
                await coin_logs.send(f"**{user}** got **{coin} {coin_e} from a bunny!**")

        elif str(payload.emoji) == "✨":
            if message.id in self.sparkle_messages:
                self.sparkle_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([2500, 5000, 10000])
                await utils.CoinFunctions.earn(earner=user, amount=coin)
                msg = await channel.send(f"{user.name} got **{coin} {coin_e}x from a sparkle!**")
                await coin_logs.send(f"**{user}** got **{coin} {coin_e} from a sparkle!**")



        else:
            return

        #! Save it to database
        async with self.bot.database() as db:
            await c.save(db)

        if msg is not None:
            await sleep(5)
            await msg.delete()
        else: 
            return


def setup(bot):
    x = Message_Rewards(bot)
    bot.add_cog(x)