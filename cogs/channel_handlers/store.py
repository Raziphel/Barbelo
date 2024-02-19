
#* Discord
from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

from math import floor

import utils


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

        embed1=Embed(description=f"# Garden Specials\n`All the listed items are worth real life money for the cost of gems!`", color=0xFF0000)
        embed1.add_field(name=f"⊰ ✨ Discord Nitro ⊱", value=f"**╰⊰ 10 {self.bot.config['gem_emoji']['hellstone']}x**\n\n```Get the 10$ Discord Nitro!```", inline=True)
        embed1.add_field(name=f"⊰ 💸 Get 5$USD! ⊱", value=f"**╰⊰ 5 {self.bot.config['gem_emoji']['hellstone']}x**\n\n```Turn all your hellstones into $USD!```", inline=True)

        embed2=Embed(description=f"# Permissions\n`All these listed items give you general permissions on the server!`", color=0x00FF00)
        embed2.add_field(name=f"⊰ 📚 Library Pass ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['sapphire']}x**\n\n```Get access to all of the server's logs!```", inline=True)
        embed2.add_field(name=f"⊰ 🎫 Image Pass ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['sapphire']}x**\n\n```Get permission for images & embeds in General Chats.```", inline=True)
        embed2.add_field(name=f"⊰ 🔊 SoundBoard Pass ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['sapphire']}x**\n\n```Get access to using the soundboard in VC!```", inline=True)
        embed2.add_field(name=f"⊰ 🎁 Stats Channel ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['ruby']}x**\n\n```Get permission to the Stats Channels!```", inline=True)
        embed2.add_field(name=f"⊰ 🧶 Thread Perms ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['ruby']}x**\n\n```Get perms to create threads!```", inline=True)
        embed2.add_field(name=f"⊰ 🔮 External Emotes ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['ruby']}x**\n\n```Get access to using your external emotes and stickers!```", inline=True)

        embed3=Embed(description=f"# Abilities\n`All these listed items give you the ability to do something here in the garden!`", color=0x0000FF)

        embed3.add_field(name=f"⊰ 🧤 Thievery ⊱", value=f"**╰⊰ 1 {self.bot.config['gem_emoji']['amethyst']}x**\n\n```Gain the ability steal from others!```", inline=True) 
        # TODO: Add a way of stealing from one another's gems and commands to be/stop being a thief!

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)







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

            #? Define Varibles
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            g = utils.Gems.get(user.id)
            mod = utils.Moderation.get(user.id)
            day = utils.Daily.get(user.id)
            items = utils.Items.get(user.id)
            #* Define Shop item
            bought = True
            item = {'name': "Unknown", 
                    'gem_type': self.bot.config['gem_emoji']['emerald'], 
                    'gem_amount': 0}


            # #? Get the correct item
            if emoji == "✨":
                item['name'] = "Discord Nitro"
                item['gem_type'] = self.bot.config['gem_emoji']['hellstone']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase Discord Nitro!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, color=0x339c2a, desc=f"# Purchase Complete\nCongrats!!!  Razi will give you your reward within 24 hours!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    razi = guild.get_member(self.bot.config['developers']['razi'])
                    await razi.send(embed=utils.Embed(user=user, color=0x339c2a, desc=f"# Discord Nitro Purchase\n{user} purchased Discord Nitro!!!!"))

            if emoji == "💸":
                item['name'] = "5$USD"
                item['gem_type'] = self.bot.config['gem_emoji']['hellstone']
                item['gem_amount'] = 5
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase 5$USD!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, color=0x339c2a, desc=f"# Purchase Complete\nCongrats!!!  Razi will give you your reward within 24 hours!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    razi = guild.get_member(self.bot.config['developers']['razi'])
                    await razi.send(embed=utils.Embed(user=user, color=0x339c2a, desc=f"# 5 dollar Purchase\n{user} purchased 5$USD!!!!"))

            if emoji == "📚":
                item['name'] = "Library Pass"
                item['gem_type'] = self.bot.config['gem_emoji']['sapphire']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase the Library Pass!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, desc=f"# Purchase Complete\nCongrats! Ya purchased a Library pass!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['library_pass'])
                    await user.add_roles(library_pass, reason="Given a Library Pass role.")

            if emoji == "🎫":
                item['name'] = "Image Pass"
                item['gem_type'] = self.bot.config['gem_emoji']['sapphire']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase the Image Pass!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, desc=f"# Purchase Complete\nCongrats! Ya purchased a Image Pass!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    image_pass = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['image_pass'])
                    await user.add_roles(image_pass, reason="Given a Image Pass role.")

            if emoji == "🔊":
                item['name'] = "Soundboard Pass"
                item['gem_type'] = self.bot.config['gem_emoji']['sapphire']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase the Soundboard Pass!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, desc=f"# Purchase Complete\nCongrats! Ya purchased a Soundboard Pass!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    soundboard_pass = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['soundboard_pass'])
                    await user.add_roles(soundboard_pass, reason="Given a Soundboard Pass role.")

            if emoji == "🎁":
                item['name'] = "Stats Channel"
                item['gem_type'] = self.bot.config['gem_emoji']['sapphire']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase the Stats Channel access\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, desc=f"# Purchase Complete\nCongrats! Ya purchased a Stats Channel access!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    stats_channel_access = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['stats_channel_access'])
                    await user.add_roles(stats_channel_access, reason="Given a Soundboard Pass role.")

            if emoji == "🧶":
                item['name'] = "Thread Permissions"
                item['gem_type'] = self.bot.config['gem_emoji']['sapphire']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase the Thread Permissions!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, desc=f"# Purchase Complete\nCongrats! Ya purchased Thread Permissions!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    threads_perm = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['threads_perm'])
                    await user.add_roles(threads_perm, reason="Given Thread Permissions role.")

            if emoji == "🔮":
                item['name'] = "External Emojis"
                item['gem_type'] = self.bot.config['gem_emoji']['sapphire']
                item['gem_amount'] = 1
                msg = await user.send(embed=utils.Embed(user=user, desc=f"# Purchase Confirmation:\nPlease confirm you would like to purchase the External Emojis!\nThis will cost you {gem_amount} {gem_type}x"))
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await msg.edit(embed=utils.Embed(user=user, desc=f"# Purchase Complete\nCongrats! Ya purchased External Emojis!"))
                    await utils.GemFunctions.payment(user=user, gem=item['gem_type'], amount=item['gem_amount'])
                    external_emojis = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['external_emojis'])
                    await user.add_roles(stats_channel_access, reason="Given External Emojis role.")


            #! Save to databse
            async with self.bot.database() as db:
                await c.save(db)
                await day.save(db)
                await mod.save(db)
                await items.save(db)

            #* Do some logging
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
                return  #* Couldn't find message in channel history

            #? See total reactions
            emoji = [i.emoji for i in message.reactions]
            if sum([i.count for i in message.reactions]) > 69:
                await message.clear_reactions()
            for e in emoji:
                await message.add_reaction(e)







    async def purchasing(self, msg, payload, item):
        '''The system for buying in the store.'''

        #? Once again get some fucking varibles defined...
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        g = utils.Gems.get(user.id)

        await msg.add_reaction("✔")
        await msg.add_reaction("❌")
        try:
            check = lambda x, y: y.id == user.id and x.message.id == msg.id and x.emoji in ["✔", "❌"]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if r.emoji == "✔":

                if item['gem_type'] == self.bot.config['gem_emoji']['hellstone']:
                    if g.hellstone < item["gem_amount"]:
                        await msg.edit(embed=utils.Embed(color=0xc74822, desc=f"You don't have enough hellstone {item['gem_type']}!"))
                        return False
                    else: return True

                if item['gem_type'] == self.bot.config['gem_emoji']['amethyst']:
                    if g.amethyst < item["gem_amount"]:
                        await msg.edit(embed=utils.Embed(color=0xc74822, desc=f"You don't have enough amethyst {item['gem_type']}!"))
                        return False
                    else: return True

                if item['gem_type'] == self.bot.config['gem_emoji']['sapphire']:
                    if g.amethyst < item["gem_amount"]:
                        await msg.edit(embed=utils.Embed(color=0xc74822, desc=f"You don't have enough sapphire {item['gem_type']}!"))
                        return False
                    else: return True

                if item['gem_type'] == self.bot.config['gem_emoji']['ruby']:
                    if g.amethyst < item["gem_amount"]:
                        await msg.edit(embed=utils.Embed(color=0xc74822, desc=f"You don't have enough ruby {item['gem_type']}!"))
                        return False
                    else: return True

            if r.emoji == "❌":
                    await msg.edit(embed=utils.Embed(color=0xc74822, desc=f"Purchase was canceled!"))
                    return False

        except TimeoutError:
            await msg.edit('Sorry, but you took too long to respond.  Transaction Canceled.', embed=None)
            return False





def setup(bot):
    x = store_Handler(bot)
    bot.add_cog(x)