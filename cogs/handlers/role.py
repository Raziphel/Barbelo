
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

        embed1=Embed(description=f"# Pronouns\n```\nYour pronouns show up under your [About Me] section.\n```\n> 🚗<@&{self.bot.config['pronouns']['she_her']}>\n> 🚓<@&{self.bot.config['pronouns']['she_they']}>\n> 🚕<@&{self.bot.config['pronouns']['he_him']}>\n> 🛺<@&{self.bot.config['pronouns']['he_they']}>\n> 🚙<@&{self.bot.config['pronouns']['they_them']}>\n> 🚌<@&{self.bot.config['pronouns']['any']}>\n> 🚐<@&{self.bot.config['pronouns']['other']}>", color=0x8f00f8)

        embed2=Embed(description=f".", color=0x8f00f8)

        embed3=Embed(description=f".", color=0x8f00f8)

        embed4=Embed(description=f".", color=0x8f00f8)

        embed5=Embed(description=f".", color=0x8f00f8)

        embed6=Embed(description=f".", color=0x8f00f8)



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
        if payload.channel_id != self.bot.config['channels']['role_handler']:
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
        role = await self.get_role(emoji=emoji, member=member, guild=guild)
        if role:
            await member.add_roles(role, reason="Role picker entry")

        # Check to see total reactions on the message
        message = await channel.fetch_message(payload.message_id)
        emoji = [i.emoji for i in message.reactions]
        if sum([i.count for i in message.reactions]) > 4000:
            await message.clear_reactions()
        for e in emoji:
            await message.add_reaction(e)

    @Cog.listener('on_raw_reaction_remove')
    async def role_remove(self, payload:RawReactionActionEvent):
        """Reaction role removal handler"""

        if payload.channel_id != self.bot.config['channels']['role_handler']:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id

        # Get the right role
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = await self.get_role(emoji=emoji, member=member, guild=guild)
        if role is None:
            return

        # Add to the user
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role, reason="Role picker entry")



    async def get_role(self, emoji, member, guild):
        """Gets the role given a picked emoji If the user has picked to enable mention alerts or VC messages, the bot will configure that _here_"""

        mod = utils.Moderation.get(member.id)
        ss = utils.Settings.get(member.id)
        role = None
        # Role picker emoji
        if emoji == "📕":
            role = utils.DiscordGet(guild.roles, name="Discord")
        elif emoji == "📗":
            role = utils.DiscordGet(guild.roles, name="Bot")
        elif emoji == "📘":
            role = utils.DiscordGet(guild.roles, name="Minecraft")

        elif emoji == "✅":
            if mod.child == False and mod.adult == False:
                mod.adult = True
                role = utils.DiscordGet(guild.roles, name="Adult 🚬")
                await member.add_roles(role)
                await self.members_log.send(embed=utils.LogEmbed(type="Special", title=f"Got Adult Role", desc=f"{member.name} was given Adult access!"))
        elif emoji == "🌼":
            if mod.child == False and mod.adult == False:
                mod.adult = True
                role = utils.DiscordGet(guild.roles, name="Adult 🍺")
                await member.add_roles(role)
                await self.members_log.send(embed=utils.LogEmbed(type="Special", title=f"Got Adult Role", desc=f"{member.name} was given Adult access!"))
        elif emoji == "❌":
            mod = utils.Moderation(member.id)
            mod.child = True
            mod.adult = False
            role = utils.DiscordGet(guild.roles, name="Child 🍼")


        elif emoji == "✨":
            role = utils.DiscordGet(guild.roles, name=".")

        elif emoji == "🐾":
            if mod.adult == True:
                role = utils.DiscordGet(guild.roles, name="*")
            else:
                role = utils.DiscordGet(guild.roles, name="-")

        elif emoji == "🌷":
            if mod.child == False and mod.adult == True:
                role = utils.DiscordGet(guild.roles, name="'")

        elif emoji == "🏹":
            role = utils.DiscordGet(guild.roles, name="|")


        elif emoji == "🎤":
            if ss.vc_msgs == True:
                ss.vc_msgs = False
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will no longer recieve messages about earning you make in vc!"))
            elif ss.vc_msgs == False:
                ss.vc_msgs = True
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will now recieve messages about earning you make in vc!"))

        elif emoji == "🔰":
            #! Need to set that up eventually
            return

        elif emoji == "⛏":
            if ss.vc_lvls == True:
                ss.vc_lvls = False
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will no longer recieve messages about leveling up in vc!"))
            elif ss.vc_lvls == False:
                ss.vc_lvls = True
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will now recieve messages about leveling up in vc!"))


        if role:
            return role

        async with self.bot.database() as db:
            await mod.save(db)
            await ss.save(db)


def setup(bot):
    x = role_handler(bot)
    bot.add_cog(x)