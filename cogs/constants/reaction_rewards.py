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
        self.hellstone_messages = []
        self.amethyst_messages = []
        self.sapphire_messages = []
        self.ruby_messages = []



    @Cog.listener('on_message')
    async def reward_gen(self, message):
        '''Message Reward Generation'''

        #? BETTER NOT BE A DM
        if message.guild == None:
            return
        #? Disables Bots
        if message.author.bot:
            return
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        #! Define some variables
        user = message.author
        messages = await message.channel.history(limit=10).flatten()

        #! Give them some rewards!
        try:
            chance = randint(1, 1000000)
            if chance <= 1:
                message = choice(messages)
                await message.add_reaction(self.bot.config['gem_emoji']['hellstone'])
                self.hellstone_messages.append(message.id)

            elif chance <= 1000:
                message = choice(messages)
                await message.add_reaction(self.bot.config['gem_emoji']['amethyst'])
                self.amethyst_messages.append(message.id)

            elif chance <= 10000:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['sapphire'])
                self.sapphire_messages.append(message.id)

            elif chance <= 100000:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['ruby'])
                self.ruby_messages.append(message.id)
        except Exception as e:
            print(f'A reward failed to spawn :: {e}')

        await sleep(10)

        try:
            await reaction.remove(self.bot.user)
        except: pass




    @Cog.listener('on_raw_reaction_add')
    async def item_reaction_handler(self, payload:RawReactionActionEvent):
        '''Handles reactions with the items'''

        #? Check if bot is connected!
        if self.bot.connected == False:
            return


        #? BETTER NOT BE A DM
        guild = self.bot.get_guild(payload.guild_id)
        user = self.bot.get_user(payload.user_id)
        if guild == None:
            return

        #? Check not a bot
        if user.bot:
            return

        #! Define Varibles
        channel = guild.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
        except: return
        msg = None

        g = utils.Gems.get(user.id)
        gem_logs = self.bot.get_channel(self.bot.config['logs']['gems'])

        if str(payload.emoji) == self.bot.config['gem_emoji']['hellstone']:
            if message.id in self.hellstone_messages:
                self.hellstone_messages.remove(message.id)
                await message.clear_reactions()
                g.hellstone += 1
                msg = await channel.send(f"{user.name} got **1 {self.bot.config['gem_emoji']['hellstone']}x**")
                await gem_logs.send(f"**{user}** got **1 {self.bot.config['gem_emoji']['hellstone']}x**")

        elif str(payload.emoji) == self.bot.config['gem_emoji']['amethyst']:
            if message.id in self.amethyst_messages:
                self.amethyst_messages.remove(message.id)
                await message.clear_reactions()
                g.amethyst += 1
                msg = await channel.send(f"{user.name} got **1 {self.bot.config['gem_emoji']['amethyst']}x**")
                await gem_logs.send(f"**{user}** got **1 {self.bot.config['gem_emoji']['amethyst']}x**")

        elif str(payload.emoji) == self.bot.config['gem_emoji']['sapphire']:
            if message.id in self.sapphire_messages:
                self.sapphire_messages.remove(message.id)
                await message.clear_reactions()
                g.sapphire += 1
                msg = await channel.send(f"{user.name} got **1 {self.bot.config['gem_emoji']['sapphire']}x**")
                await gem_logs.send(f"**{user}** got **1 {self.bot.config['gem_emoji']['sapphire']}x**")

        elif str(payload.emoji) == self.bot.config['gem_emoji']['ruby']:
            if message.id in self.ruby_messages:
                self.ruby_messages.remove(message.id)
                await message.clear_reactions()
                g.ruby += 1
                msg = await channel.send(f"{user.name} got **1 {self.bot.config['gem_emoji']['ruby']}x**")
                await gem_logs.send(f"**{user}** got **1 {self.bot.config['gem_emoji']['ruby']}x**")


        else: 
            return

        #! Save it to database
        async with self.bot.database() as db:
            await g.save(db)

        if msg != None:
            await sleep(5)
            await msg.delete()
        else: 
            return


def setup(bot):
    x = Message_Rewards(bot)
    bot.add_cog(x)