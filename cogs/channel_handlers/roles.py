
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
        """Displays the role handler messages"""
        ch = self.bot.get_channel(self.bot.config['channels']['roles'])

        msg1 = await ch.fetch_message(self.bot.config['roles_messages']['1']) 
        msg2 = await ch.fetch_message(self.bot.config['roles_messages']['2'])
        msg3 = await ch.fetch_message(self.bot.config['roles_messages']['3'])
        msg4 = await ch.fetch_message(self.bot.config['roles_messages']['4'])
        msg5 = await ch.fetch_message(self.bot.config['roles_messages']['5'])
        msg6 = await ch.fetch_message(self.bot.config['roles_messages']['6'])

        embed1=Embed(description=f"# Age\n```\nLying about your age will result in a ban!\n```\n> 🚬<@&{self.bot.config['age_roles']['adult']}>`Gives access to adult only channels!`\n> 🍼<@&{self.bot.config['age_roles']['underage']}>`Given automatically if you don't get an age role.`", color=0x8f00f8)

        embed2=Embed(description=f"# Pings\n```\nGet notifications for things!\n```\n> 📔<@&{self.bot.config['ping_roles']['changelogs']}> `Recommended! Get pinged about changes!`\n> ✅<@&{self.bot.config['ping_roles']['voters']}> `Get pinged when a vote is held!`\n> 📆<@&{self.bot.config['ping_roles']['events']}> `Get pinged for info on server events!`\n> 🤝<@&{self.bot.config['ping_roles']['welcomer']}> `Get pinged to greet any new members!`\n> 📊<@&{self.bot.config['ping_roles']['server_status']}> `Get pinged when our servers are down!`", color=0x8f00f8)

        embed3=Embed(description=f"# Access\n```\nWhat parts of the server would you like to see!\n```\n> 🚧<@&{self.bot.config['access_roles']['scpsl']}>`Gives access to SCP:SL section.`\n> 🎀<@&{self.bot.config['access_roles']['queer']}>`Gives access to Queer, Furry and degens section.`\n> 🚬<@&{self.bot.config['access_roles']['shitposters']}>`Gives access to Toxic shitters section.`", color=0x8f00f8)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f"~")
        await msg5.edit(content=f"~")
        await msg6.edit(content=f"~")




    @Cog.listener('on_raw_reaction_add')
    async def role_add(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        # Validate channel
        if payload.channel_id != self.bot.config['channels']['roles']:
            return

        # Not bot
        if self.bot.get_user(payload.user_id).bot:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id


        # Work out cached items
        channel = self.bot.get_channel(payload.channel_id)
        guild = channel.guild
        member = guild.get_member(payload.user_id)

        # Get the right role
        role = await self.get_role(guild=guild, emoji=emoji, member=member)
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

        if payload.channel_id != self.bot.config['channels']['roles']:
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
        mod = utils.Moderation.get(member.id)
        if emoji == "🚬":
            if not mod.child:
                role = utils.DiscordGet(guild.roles, id=self.bot.config['age_roles']['adult'])
            else: 
                await member.send(f"You are unable to get the Adult role, message staff.")
                await self.discord_log.send(f"<@{member.id}> failed to get ADULT role.")
        elif emoji == "🍼":
            if not mod.adult:
                role = utils.DiscordGet(guild.roles, id=self.bot.config['age_roles']['underage'])
            else: 
                await member.send(f"You are unable to get the Child role, message staff.")
                await self.discord_log.send(f"<@{member.id}> failed to get CHILD role.")

        if emoji == "📔":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['changelogs'])
        elif emoji == "✅":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['voters'])
        elif emoji == "📆":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['events'])
        elif emoji == "🤝":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['welcomer'])
        elif emoji == "📊":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['server_status'])
        elif emoji == "🍎":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['ping_me'])

        elif emoji == "🚧":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['access_roles']['scpsl'])
        elif emoji == "🎀":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['access_roles']['queer'])
        elif emoji == "🚬":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['access_roles']['shitposters'])

        if role:
            return role



def setup(bot):
    x = role_handler(bot)
    bot.add_cog(x)