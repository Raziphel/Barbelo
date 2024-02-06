
from discord import Embed, Member, Message, RawReactionActionEvent  
from discord.ext.commands import Cog 

import utils


class role_handler(Cog): 
    def __init__(self, bot):
        self.bot = bot


    @property  #+ The Server Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 


    @Cog.listener()
    async def on_ready(self):
        '''Displays the role handler messages'''
        ch = self.bot.get_channel(self.bot.config['channels']['roles'])

        msg1 = await ch.fetch_message(self.bot.config['role_handler']['1']) 
        msg2 = await ch.fetch_message(self.bot.config['role_handler']['2'])
        msg3 = await ch.fetch_message(self.bot.config['role_handler']['3'])
        msg4 = await ch.fetch_message(self.bot.config['role_handler']['4'])
        msg5 = await ch.fetch_message(self.bot.config['role_handler']['5'])
        msg6 = await ch.fetch_message(self.bot.config['role_handler']['6'])

        embed1=Embed(description=f"# Pronouns\n> 💜<@&{self.bot.config['pronoun_roles']['she_her']}>\n> 💛<@&{self.bot.config['pronoun_roles']['she_they']}>\n> 💙<@&{self.bot.config['pronoun_roles']['he_him']}>\n> 💚<@&{self.bot.config['pronoun_roles']['he_they']}>\n> 🧡<@&{self.bot.config['pronoun_roles']['they_them']}>\n> 🤍<@&{self.bot.config['pronoun_roles']['any']}>\n> 🤎<@&{self.bot.config['pronoun_roles']['other']}>", color=0x8f00f8)

        embed2=Embed(description=f"# DM Preference\n> 🟢<@&{self.bot.config['dm_roles']['open']}>\n> 🟡<@&{self.bot.config['dm_roles']['ask']}>\n> 🔴<@&{self.bot.config['dm_roles']['closed']}>", color=0x8f00f8)

        embed3=Embed(description=f"# LGBTQ Pride\n> {self.bot.config['lgbt_emoji']['trans']}<@&{self.bot.config['lgbt_roles']['trans']}>\n> {self.bot.config['lgbt_emoji']['binary']}<@&{self.bot.config['lgbt_roles']['binary']}>\n> {self.bot.config['lgbt_emoji']['pan']}<@&{self.bot.config['lgbt_roles']['pan']}>\n> :rainbow_flag:<@&{self.bot.config['lgbt_roles']['gay']}>\n> {self.bot.config['lgbt_emoji']['lesbian']}<@&{self.bot.config['lgbt_roles']['lesbian']}>\n> {self.bot.config['lgbt_emoji']['asexual']}<@&{self.bot.config['lgbt_roles']['asexual']}>\n> {self.bot.config['lgbt_emoji']['bi']}<@&{self.bot.config['lgbt_roles']['bi']}>", color=0x8f00f8)

        embed4=Embed(description=f"# Age\n```\nLying about your age will result in a ban!\nKeep in mind nsfw mostly contains furry art.\n```\n> 🍺<@&{self.bot.config['age_roles']['nsfw_adult']}> `Gives access to NSFW text & voice channels.`\n> 🚬<@&{self.bot.config['age_roles']['adult']}>`Only gives access to NSFW voice channels.`\n> 🍼<@&{self.bot.config['age_roles']['underage']}>`Is given automatically if you don't get an age role.`", color=0x8f00f8)

        embed5=Embed(description=f"# Pings\n> 📔<@&{self.bot.config['ping_roles']['changelogs']}> `Recommended! Get pinged about changes!`\n> ✅<@&{self.bot.config['ping_roles']['voters']}> `Get pinged when a vote is held!`\n> 📆<@&{self.bot.config['ping_roles']['events']}> `Get pinged for info on server events!`\n> 🎲<@&{self.bot.config['ping_roles']['gambler']}> `Get a ping to see who won raffles.`\n> 🤝<@&{self.bot.config['ping_roles']['welcomer']}> `Get pinged to greet any new members!`\n> 🔦<@&{self.bot.config['ping_roles']['lethal']}> `Anyone can ping this role using /sendping`\n> 🔒<@&{self.bot.config['ping_roles']['scp']}> `Anyone can ping this role using /sendping`\n> 🔊<@&{self.bot.config['ping_roles']['vc']}> `Anyone can ping this role using /sendping`", color=0x8f00f8)

        embed6=Embed(description=f"# Color roles\n```\nBetter colors are available in the #╰⊰🛒store\n```\n> 🍎<@&{self.bot.config['color_roles']['red_apple']}>\n> 🍏<@&{self.bot.config['color_roles']['green_apple']}>\n> 🍑<@&{self.bot.config['color_roles']['peach']}>\n> 🥕<@&{self.bot.config['color_roles']['carrot']}>", color=0x8f00f8)



        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)
        await msg6.edit(content=f" ", embed=embed6)




    @Cog.listener('on_raw_reaction_add')
    async def role_add(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        # Validate channel
        if payload.channel_id != self.bot.config['channels']['royale']['role_handler']:
            return

        # Not bot
        if self.bot.get_user(payload.user_id).bot:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id

        # Work out out cached items
        channel = self.bot.get_channel(payload.channel_id)
        guild = channel.guild
        member = guild.get_member(payload.user_id)

        # Get the right role
        role = await self.get_role(guild=guild, emoji=emoji, member=member)
        if role:
            await member.add_roles(role, reason="Role picker entry")

            # Check they only have one gender role
            gender_roles = self.bot.config['pronoun_roles'].values()
            if len([i for i in member.roles if i.id in gender_roles]) > 1:
                try:
                    for i in gender_roles:
                        role = utils.DiscordGet(guild.roles, name=i)
                        await member.remove_roles(role, reason="Too many pronoun roles")
                except Exception:
                    pass
                return

            # Check they only have one DM role
            dm_roles = self.bot.config['dm_roles'].values()
            if len([i for i in member.roles if i.name in dm_roles]) > 1:
                await member.send(f"You can only have one DM preference.")
                try:
                    for i in dm_roles:
                        role = utils.DiscordGet(guild.roles, name=i)
                        await member.remove_roles(role, reason="Too many DM roles")
                except Exception:
                    pass
                return

            # Check they only have one color role
            color_roles = self.bot.config['color_roles'].values()
            if len([i for i in member.roles if i.name in color_roles]) > 1:
                await member.send(f"You can only have one color role at a time.")
                try:
                    for i in color_roles:
                        role = utils.DiscordGet(guild.roles, name=i)
                        await member.remove_roles(role, reason="Too many color roles")
                except Exception:
                    pass
                return

        # Check to see total reactions on the message
        message = await channel.fetch_message(payload.message_id)
        emoji = [i.emoji for i in message.reactions]
        if sum([i.count for i in message.reactions]) > 200:
            await message.clear_reactions()
        for e in emoji:
            await message.add_reaction(e)

    @Cog.listener('on_raw_reaction_remove')
    async def role_remove(self, payload:RawReactionActionEvent):
        """Reaction role removal handler"""

        if payload.channel_id != self.bot.config['channels']['royale']['role_handler']:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id

        # Get the right role
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = await self.get_role(guild=guild, emoji=emoji, member=member)
        if role is None:
            return

        # Add to the user
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role, reason="Role picker entry")



    async def get_role(self, guild, emoji, member):
        """Gets the role given a picked emoji If the user has picked to enable mention alerts or VC messages, the bot will configure that _here_"""

        role = None
        # Role picker emoji
        if emoji == "💜":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['she_her'])
        elif emoji == "💛":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['she_they'])
        elif emoji == "💙":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['he_him'])
        elif emoji == "💚":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['he_they'])
        elif emoji == "🧡":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['they_them'])
        elif emoji == "🤍":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['any'])
        elif emoji == "🤎":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['pronoun_roles']['other'])

        elif emoji == "🌈":
            role = utils.DiscordGet(guild.roles, name="Gay / Lesbian")
        elif emoji == "🍳":
            role = utils.DiscordGet(guild.roles, name="Pansexual / Demisexual")
        elif emoji == "📏":
            role = utils.DiscordGet(guild.roles, name="Straight")
        elif emoji == "🎈":
            role = utils.DiscordGet(guild.roles, name="Bisexual")
        elif emoji == "😔":
            role = utils.DiscordGet(guild.roles, name="Asexual")

        elif emoji == "🎮":
            role = utils.DiscordGet(guild.roles, name="Gamer")
        elif emoji == "📸":
            role = utils.DiscordGet(guild.roles, name="Youtuber")
        elif emoji == "🎦":
            role = utils.DiscordGet(guild.roles, name="Streamer")
        elif emoji == "🎨":
            role = utils.DiscordGet(guild.roles, name="Artist")
        elif emoji == "🐎":
            role = utils.DiscordGet(guild.roles, name="MLP")
        elif emoji == "🎀":
            role = utils.DiscordGet(guild.roles, name="Femboy")
        elif emoji == "🐁":
            role = utils.DiscordGet(guild.roles, name="Trap >///<")
        elif emoji == "🎑":
            role = utils.DiscordGet(guild.roles, name="Anime Slut")
        elif emoji == "🧸":
            role = utils.DiscordGet(guild.roles, name="Plushie")
        elif emoji == "⛏":
            role = utils.DiscordGet(guild.roles, name="Minecraft")
        elif emoji == "🥽":
            role = utils.DiscordGet(guild.roles, name="VR Chat")

        elif emoji == "👸":
            role = utils.DiscordGet(guild.roles, name="Wanna be princess")
        elif emoji == "💸":
            role = utils.DiscordGet(guild.roles, name="Meanie Memey")
        elif emoji == "🐕":
            role = utils.DiscordGet(guild.roles, name="Feral")

        elif emoji == "1️⃣":
            role = utils.DiscordGet(guild.roles, name="Africa")
        elif emoji == "2️⃣":
            role = utils.DiscordGet(guild.roles, name="Western Asia")
        elif emoji == "3️⃣":
            role = utils.DiscordGet(guild.roles, name="Europe Nordic & East")
        elif emoji == "4️⃣":
            role = utils.DiscordGet(guild.roles, name="Europe West")
        elif emoji == "5️⃣":
            role = utils.DiscordGet(guild.roles, name="North America")
        elif emoji == "6️⃣":
            role = utils.DiscordGet(guild.roles, name="South America")
        elif emoji == "7️⃣":
            role = utils.DiscordGet(guild.roles, name="Oceania")
        elif emoji == "8️⃣":
            role = utils.DiscordGet(guild.roles, name="Pacific Islands")
        elif emoji == "9️⃣":
            role = utils.DiscordGet(guild.roles, name="Russia")
        elif emoji == "0️⃣":
            role = utils.DiscordGet(guild.roles, name="Eastern Asia")

        mod = utils.Moderation.get(member.id)
        if mod.nsfw == True:
            if emoji == "🍒":
                role = utils.DiscordGet(guild.roles, name="Femboy")
            elif emoji == "🥞":
                role = utils.DiscordGet(guild.roles, name="Tomboy")
            elif emoji == "🥨":
                role = utils.DiscordGet(guild.roles, name="Trap")
            elif emoji == "🍩":
                role = utils.DiscordGet(guild.roles, name="Brat")
            elif emoji == "1️⃣":
                role = utils.DiscordGet(guild.roles, name="Single")
            elif emoji == "2️⃣":
                role = utils.DiscordGet(guild.roles, name="Taken")
            elif emoji == "🌺":
                role = utils.DiscordGet(guild.roles, name="Sub")
            elif emoji == "🥓":
                role = utils.DiscordGet(guild.roles, name="Dom")

        if role:
            return role

        # User settings change
        ss = utils.Settings.get(member.id)

        # VC messages
        if emoji == "🎤":
            if ss.vc_msgs is True:
                ss.vc_msgs = False
            else:
                ss.vc_msgs = True
            async with self.bot.database() as db:
                await ss.save(db)
            await member.send(embed=utils.LogEmbed(type="special", title=f"VC MSGS: {ss.vc_msgs}"))

        elif emoji == "✅":
            mod = utils.Moderation.get(member.id)
            if mod.nsfw == False:
                if guild.id == self.bot.config['guilds']['RaziRealmID']:
                    role = utils.DiscordGet(guild.roles, name="Adult 🚬")
                elif guild.id == self.bot.config['guilds']['FurryRoyaleID']:
                    role = utils.DiscordGet(guild.roles, name="18+")
                await member.add_roles(role)
                log = await utils.ChannelFunction.get_log_channel(guild=member.guild, log="member")
                await log.send(embed=utils.LogEmbed(type="Special", title=f"Got Adult Role", desc=f"{member.name} was given nsfw access!"))



def setup(bot):
    x = role_handler(bot)
    bot.add_cog(x)