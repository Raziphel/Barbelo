
#* Discord
from math import floor

from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

import utils


# * Additions

class store_Handler(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #! The currency logs
    def gem_logs(self):
        return self.bot.get_channel(self.bot.config['logs']['gems'])


    @Cog.listener('on_ready')
    async def store_msg(self):
        ch = self.bot.get_channel(self.bot.config['channels']['store'])

        msg1 = await ch.fetch_message(self.bot.config['store_messages']['1']) 
        msg2 = await ch.fetch_message(self.bot.config['store_messages']['2'])
        msg3 = await ch.fetch_message(self.bot.config['store_messages']['3'])
        msg4 = await ch.fetch_message(self.bot.config['store_messages']['4'])
        msg5 = await ch.fetch_message(self.bot.config['store_messages']['5'])
        msg6 = await ch.fetch_message(self.bot.config['store_messages']['6'])

        embed1=Embed(description=f"# Garden Specials\n`All the listed items are worth real life money for the cost of gems!`", color=0x80F75C)
        embed1.add_field(name=f"✨ ❧ Discord Nitro", value=f"**10x {self.bot.config['gem_emoji']['hellstone']}**\n\n```Get the 10$ Discord Nitro!```", inline=True)
        embed1.add_field(name=f"💲 ❧ 5$ USD", value=f"**5x {self.bot.config['gem_emoji']['hellstone']}**\n\n```Get paypal'd 5$ USD!```", inline=True)

        await msg1.edit(content=f" ", embed=embed1)







    @Cog.listener('on_raw_reaction_add')
    async def store_buy(self, payload:RawReactionActionEvent):
            '''Buys item's from the store.'''

            #! See if I need to deal with it
            if not payload.channel_id == self.bot.config['channels']['store']:
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            #! See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji.id

            #* Get the coin emojis
            coin = self.bot.config['emotes']['coin']


            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            c = utils.Currency.get(user.id)
            mod = utils.Moderation.get(user.id)
            day = utils.Daily.get(user.id)
            items = utils.Items.get(user.id)
            bought = False
            item = {"name": "BROKEN OH NO", "coin": -1}

            #? Get the correct item
            if emoji == "✨":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase Discord Nitro!\nCost: {coin} 1,000,000x", footer=" "))
                item['coin'] = 1000000
                item['name'] = "Discord Nitro"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats!!!  Razi will give you your reward within 24 hours!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    razi = guild.get_member(self.bot.config['developers']['razi'])
                    await razi.send(embed=utils.LogEmbed(type="special", title="Discord Nitro Purchase", desc=f"{user} purchased Discord Nitro!!!!", footer=" "))

            if emoji == "📚":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Library Pass!\nCost: {coin} 40,000x", footer=" "))
                item['coin'] = 40000
                item['name'] = "Library Pass"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a Library pass!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['library_pass'])
                    await user.add_roles(library_pass, reason="Given a Library Pass role.")

            if emoji == "🎫":
                if mod.image_banned == True:
                    await user.send(embed=utils.LogEmbed(type="special", title="IMAGE BANNED", desc=f"You have been banned from ever being able to have an image pass! <3", footer=" "))
                    return
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Image Pass!\nCost: {coin} 50,000x", footer=" "))
                item['coin'] = 50000
                item['name'] = "Image Pass"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a Image pass!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    image_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['image_pass'])
                    await user.add_roles(image_pass, reason="Given a Image Pass role.")

            if emoji == "🎁":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Stat Channels!\nCost: {coin} 10,000x", footer=" "))
                item['coin'] = 10000
                item['name'] = "Stats Channel"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Stat Channels!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    special = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['specials'])
                    await user.add_roles(special, reason="Given the Stat Channels role.")

            if emoji == "🔥":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the dungeon key!\nCost: {coin} 30,000x", footer=" "))
                item['coin'] = 30000
                item['name'] = "dungeon key"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the dungeon key!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    automod = utils.DiscordGet(guild.roles, id=1095177740451323984)
                    await user.add_roles(automod, reason="Given dungeon key role.")

            if emoji == "🔊":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Sound Board Access!\nCost: {coin} 50,000x", footer=" "))
                item['coin'] = 50000
                item['name'] = "Sound Board Access"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Sound Board Access!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    automod = utils.DiscordGet(guild.roles, id=1137618537020665910)
                    await user.add_roles(automod, reason="Given SoundBoard key role.")

            if emoji == "💎":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Daily Bonus!\nCost: {coin} 40,000x", footer=" "))
                item['coin'] = 40000
                item['name'] = "Daily Bonus"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a daily bonus!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    day.premium = True

            if emoji == "🧤":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 5 thief gloves!\nCost: {coin} 20,000x", footer=" "))
                item['coin'] = 20000
                item['name'] = "5 thief gloves"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased 5 thief gloves!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    items.thief_gloves += 5

            if emoji == "🧶":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Thread Perms.\nCost: {coin} 20,000x", footer=" "))
                item['coin'] = 20000
                item['name'] = "Thread Perms"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Thread Perms!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    thread_perms = utils.DiscordGet(guild.roles, id=1186717217501487225)
                    await user.add_roles(thread_perms, reason="Given thread perms.")

            if emoji == "🎈":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Reaction Perms!\nCost: {coin} 20,000x", footer=" "))
                item['coin'] = 20000
                item['name'] = "Reaction Perms"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Reaction Perms!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    bottom = utils.DiscordGet(guild.roles, id=1186714161405771838)
                    await user.add_roles(bottom, reason="Given Reaction Perms.")


            if emoji == "🔮":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase External Emotes/Stickers!\nCost: {coin} 30,000x", footer=" "))
                item['coin'] = 30000
                item['name'] = "External Emotes/Stickers"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Goblin Badge on SCP servers!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    coin_goblin = utils.DiscordGet(guild.roles, id=1186714489022849034)
                    await user.add_roles(coin_goblin, reason="Given External Emotes/Stickers")



            #! Save to databse
            async with self.bot.database() as db:
                await c.save(db)
                await day.save(db)
                await mod.save(db)
                await items.save(db)


            if bought == True:
                await self.coin_logs.send(f"**{user}** bought **{item['name']}**!")
            else: 
                await self.coin_logs.send(f"**{user}** tried to purchase: **{item['name']}**")

            #! Check to see total reactions on the message
            channel_id = payload.channel_id
            channel = self.bot.get_channel(channel_id)
            async for message in channel.history():
                if message.id == payload.message_id:
                    break 
            if message.id != payload.message_id:
                return  # Couldn't find message in channel history

            # See total reactions
            emoji = [i.emoji for i in message.reactions]
            if sum([i.count for i in message.reactions]) > 69:
                await message.clear_reactions()
            for e in emoji:
                await message.add_reaction(e)



    async def purchasing(self, msg, payload, item):
        '''The system for buying in the store.'''

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        c = utils.Currency.get(user.id)
        coin = self.bot.config['emotes']['coin']


        await msg.add_reaction("✔")
        await msg.add_reaction("❌")
        try:
            check = lambda x, y: y.id == user.id and x.message.id == msg.id and x.emoji in ["✔", "❌"]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if r.emoji == "✔":
                if c.coins < item["coin"]:
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"You don't have enough Coins for: `{item['name']}`!\nYou need {item['coin'] - floor(c.coins):,}x {coin}!", footer=" "))
                    return False
                else: return True

            if r.emoji == "❌":
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"Purchase was canceled!", footer=" "))
                    return False


        except TimeoutError:
            await msg.edit('Sorry, but you took too long to respond.  Transaction Canceled.', embed=None)
            return False




def setup(bot):
    x = store_Handler(bot)
    bot.add_cog(x)