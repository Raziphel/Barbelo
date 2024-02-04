
#* Discord
from discord.ext.commands import Cog
#* Additions
from random import randint
import math

import utils

class Logging(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #+ The Server Logs
    def bot_log(self):
        return self.bot.get_channel(self.bot.config['logs']['bot']) 

    @property  #+ The Members Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 

    @property  #+ The Message Logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['logs']['messages']) 

    @property  #+ The Staff Logs
    def staff_log(self):
        return self.bot.get_channel(self.bot.config['logs']['staff'])

    @property  #+ The Adult Logs
    def adult_log(self):
        return self.bot.get_channel(self.bot.config['logs']['adult'])

    @property  #+ The Welcome Logs
    def welcome_log(self):
        return self.bot.get_channel(self.bot.config['channels']['general'])



#? ---  COLOR PICKER  ---
#? 
#? GREEN -> 0x339c2a ... Positive logs
#? RED -> 0xc74822 ... Negative logs
#? WARN -> 0xc77f22 ... Warning logs
#? SPECIAL -> randint(1, 0xffffff)
#? 


    #! Brand new members joining 
    @Cog.listener()
    async def on_member_join(self, member):

        #+ Assign new member roles.
        guild = self.bot.get_guild(self.bot.config['guild_id'])
        seperator_role_ids = [self.bot.config['seperator_roles']['access'], 
                            self.bot.config['seperator_roles']['purchases'], 
                            self.bot.config['seperator_roles']['pings'], 
                            self.bot.config['seperator_roles']['about']]
        for role_id in seperator_role_ids:
            role = utils.DiscordGet(guild.roles, id=role_id)
            await user.add_roles(role, reason="Joined Server!")

        #+ Send joining server messages!
        try:
            #? General Welcome Message!
            await self.welcome_log.send(content=f"<@&{self.bot.config['ping_roles']['welcomer']}> {user.mention}", 
                                        embed=utils.Embed(color=randint(1, 0xffffff), title=f"{member.name} has joined the cult."))
            #? Log
            await self.discord_log.send(embed=utils.Embed(color=0x339c2a, title=f"{member.name} has joined the cult.", thumbnail=member.avatar.url))
        except: pass



    #! Logs
    @Cog.listener()
    async def on_ready(self):
        print('The Baphomet is now online.')

        #+ Secret bullshit bro...  Don't question this...
        if math.floor(self.bot.latency*1000) <= 100: 
            await self.bot_log.send(embed=utils.Embed(color=0x339c2a, title=f"Baphomet is Online!", desc=f"Perfect Restart."))
        elif math.floor(self.bot.latency*1000) <= 420:
            await self.bot_log.send(embed=utils.Embed(color=0xc74822, title=f"Baphomet is Online!", desc=f"Weird Restart."))
        elif math.floor(self.bot.latency*1000) > 200:
            await self.bot_log.send(embed=utils.Embed(color=0xc77f22, title=f"Baphomet is Online!", desc=f"Discord Connection Refresh"))


    @Cog.listener()
    async def on_guild_join(self, guild):
        user_count = len(set(self.bot.get_all_members()))
        await self.bot_log.send(embed=utils.Embed(color=0x339c2a, title=f"The bot has joined {guild.name}", desc=f"Bot now manages: {user_count:,} users"))
        

    @Cog.listener()
    async def on_guild_remove(self, guild):
        user_count = len(set(self.bot.get_all_members()))
        await self.bot_log.send(embed=utils.Embed(color=0xc74822, title=f"The bot has left {guild.name}", desc=f"Bot now manages: {user_count:,} users"))

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot_log.send(f"Command failed - `{error!s}`;")
        raise error



    #! Guild Logs
    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            if member.bot: return
            await self.discord_log.send(embed=utils.Embed(color=0xc74822, title=f"{member.name} has left the Cult.", thumbnail=member.avatar.url))
            c = utils.Currency.get(member.id)
            c.coins = 0
            async with self.bot.database() as db:
                await c.save(db)
        except: pass #? Fail Silently


    @Cog.listener()
    async def on_member_ban(self, guild, member):
        try:
            await self.discord_log.send(embed=utils.Embed(color=0xc77f22, title=f"Member Banned", desc=f"{member} has been banned!"))
        except: pass #? Fail Silently


    @Cog.listener()
    async def on_member_unban(self, guild, member):
        try:
            await self.discord_log.send(embed=utils.Embed(color=0x339c2a, title=f"Member Unbanned", desc=f"{member} has been unbanned!"))
        except: pass #? Fail Silently


    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return #? Check it's not a bot.
        image = None
        if message is None:
            return #? Check its a message with content?
        if message.channel.name is None:
            return #? Check it's a channel.
        if message.author.id == 159516156728836097: 
            return #? Not Razi tho.
        if message.attachments: 
            image = message.attachments[0].url 
        name_list = list(message.channel.name)

        if any(item in name_list for item in ['🍺', "🐇", "🎀"]):
            channel = self.adult_log
        elif any(item in name_list for item in ['🔥', "✨"]):
            channel = self.staff_log
        elif any(item in name_list for item in ['👑', "🌷", "📯", "📝"]):
            return
        else: channel = self.message_log

        try:
            await channel.send(embed=utils.Embed(color=0xc74822, title=f"Message Deleted", desc=f"\"{message.content}\"\n**Channel:** <#{message.channel.id}>\n**Author:** {message.author.mention}", thumbnail=message.author.avatar.url, image=image))
        except: pass



    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: return
        if before.content == after.content: return
        if before.author.id == 159516156728836097: return #? Not Razi tho
        name_list = list(before.channel.name)

        if any(item in name_list for item in ['🍺', "🐇", "🎀"]):
            channel = self.adult_log
        elif any(item in name_list for item in ['🔥', "✨"]):
            channel = self.staff_log
        elif any(item in name_list for item in ['👑', "🌷", "📯", "📝"]):
            return
        else: channel = self.message_log
        try:
            await channel.send(embed=utils.Embed(color=0xc77f22, title=f"Message Edited", desc=f"**Author:** {before.author.mention}\n**Channel:** <#{before.channel.id}>\n**Before:**\n{before.content}\n\n**after:**\n{after.content}", thumbnail=before.author.avatar.url))
        except: pass

    @Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        try:
            await self.message_log.send(embed=utils.Embed(type=randint(1, 0xffffff), title=f"Message Pinned", desc=f"A pinned in: <#{channel.id}>\n{last_pin} was made/modify!"))
        except: pass #? Fail Silently





def setup(bot):
    x = Logging(bot)
    bot.add_cog(x)
