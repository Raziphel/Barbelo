
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

        msg1 = await ch.fetch_message(self.bot.config['roles_messages']['1']) 
        msg2 = await ch.fetch_message(self.bot.config['roles_messages']['2'])
        msg3 = await ch.fetch_message(self.bot.config['roles_messages']['3'])
        msg4 = await ch.fetch_message(self.bot.config['roles_messages']['4'])
        msg5 = await ch.fetch_message(self.bot.config['roles_messages']['5'])
        msg6 = await ch.fetch_message(self.bot.config['roles_messages']['6'])

        embed1=Embed(description=f"# Age\n```\nLying about your age will result in a ban!\n```\n> 🚬<@&{self.bot.config['age_roles']['adult']}>`Gives access to adult only channels!`\n> 🍼<@&{self.bot.config['age_roles']['underage']}>`Is given automatically if you don't get an age role.`", color=0x8f00f8)

        embed2=Embed(description=f"# Pings\n> 📔<@&{self.bot.config['ping_roles']['changelogs']}> `Recommended! Get pinged about changes!`\n> ✅<@&{self.bot.config['ping_roles']['voters']}> `Get pinged when a vote is held!`\n> 📆<@&{self.bot.config['ping_roles']['events']}> `Get pinged for info on server events!`\n> 🤝<@&{self.bot.config['ping_roles']['welcomer']}> `Get pinged to greet any new members!`", color=0x8f00f8)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f"~")
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


        # Work out out cached items
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

        if emoji == "🟢":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['dm_roles']['open'])
        elif emoji == "🟡":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['dm_roles']['ask'])
        elif emoji == "🔴":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['dm_roles']['closed'])

        mod = utils.Moderation.get(member.id)
        if emoji == "🚬":
            if mod.child != True:
                role = utils.DiscordGet(guild.roles, id=self.bot.config['age_roles']['adult'])
            else: 
                await member.send(f"You are unable to get the Adult role, message staff.")
                await self.discord_log.send(f"<@{member.id}> failed to get ADULT role.")
        elif emoji == "🍼":
            if mod.adult != True:
                role = utils.DiscordGet(guild.roles, id=self.bot.config['age_roles']['underage'])
            else: 
                await member.send(f"You are unable to get the Child role, message staff.")
                await self.discord_log.send(f"<@{member.id}> failed to get CHILD role.")

        if emoji == 1140458935694934037:
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['trans'])
        elif emoji == 1145387497199763486:
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['binary'])
        elif emoji == 1139231865547530280:
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['pan'])
        elif emoji == "🌈":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['gay'])
        elif emoji == 1141807570915434507:
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['lesbian'])
        elif emoji == 1140089833692336128:
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['asexual'])
        elif emoji == 1141808161980956762:
            role = utils.DiscordGet(guild.roles, id=self.bot.config['lgbt_roles']['bi'])

        if emoji == "📔":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['changelogs'])
        elif emoji == "✅":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['voters'])
        elif emoji == "📆":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['events'])
        if emoji == "🎲":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['gambler'])
        elif emoji == "🤝":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['welcomer'])
        elif emoji == "🔦":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['lethal'])
        elif emoji == "🔒":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['scp'])
        elif emoji == "🔊":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['ping_roles']['vc'])

        if emoji == "🍎":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['color_roles']['red_apple'])
        elif emoji == "🍏":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['color_roles']['green_apple'])
        elif emoji == "🍑":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['color_roles']['peach'])
        elif emoji == "🥕":
            role = utils.DiscordGet(guild.roles, id=self.bot.config['color_roles']['carrot'])

        # mod = utils.Moderation.get(member.id)
        # if mod.nsfw == True:
        #     if emoji == "🍒":
        #         role = utils.DiscordGet(guild.roles, name="Femboy")
        #     elif emoji == "🥞":
        #         role = utils.DiscordGet(guild.roles, name="Tomboy")
        #     elif emoji == "🥨":
        #         role = utils.DiscordGet(guild.roles, name="Trap")
        #     elif emoji == "🍩":
        #         role = utils.DiscordGet(guild.roles, name="Brat")
        #     elif emoji == "1️⃣":
        #         role = utils.DiscordGet(guild.roles, name="Single")
        #     elif emoji == "2️⃣":
        #         role = utils.DiscordGet(guild.roles, name="Taken")
        #     elif emoji == "🌺":
        #         role = utils.DiscordGet(guild.roles, name="Sub")
        #     elif emoji == "🥓":
        #         role = utils.DiscordGet(guild.roles, name="Dom")

        if role:
            return role



def setup(bot):
    x = role_handler(bot)
    bot.add_cog(x)