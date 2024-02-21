# * Discord
from discord import ApplicationCommandOption, ApplicationCommandOptionType
from discord import Member, User, Embed
from discord.ext.commands import ApplicationCommandMeta
from discord.ext.commands import command, Cog

# * Additions
import utils
from typing import Optional


class Staff_Actions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #+ The Message Logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['logs']['messages']) 

    @property  #+ The Members Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 





    @utils.is_admin_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be banned from the server!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="reason",
                    description="The reason for being banned!",
                    type=ApplicationCommandOptionType.string,
                    required=True,
                ),
            ],
        ),
    )
    async def ban(self, ctx, user:Member, *, reason:Optional[str]="[No Reason Given]"):
        '''Bans any given amount of members given!'''

        if not user:
            return await ctx.interaction.response.send_message('Please specify a valid user.')

        #+ Ban that loser!
        if user:
            #! Ban hammer message
            try:
                await user.send(F"# Sorry, you were banned from {ctx.guild} for: {reason}\n\n**Honestly that's a rip...**\n**I doubt you will be missed tho! c:**")
            except: pass
            await ctx.guild.ban(user, delete_message_days=0, reason=f'{reason} :: banned by {ctx.author!s}')

        #! Report who has been banned!
        await ctx.interaction.response.send_message(embed=utils.Embed(color=0xc77f22, desc=f"# {user.name} has been banned!**\nBy: {ctx.author}\nReason :: {reason}"))
        await self.discord_log.send(embed=utils.Embed(color=0xc77f22, desc=f"# {user.name} has been banned!**\nBy: {ctx.author}\nReason :: {reason}"))







    @utils.is_mod_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be permenantly banned from using the image pass!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                )
            ],
        ),
    )
    async def imageban(self, ctx, user:Member):
        '''Bans a user from posting images.'''  
        mod = utils.Moderation.get(user.id)
        mod.image_banned = True
        async with self.bot.database() as db:
            await mod.save(db)

        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild

        image_pass = utils.DiscordGet(guild.roles, id=self.bot.config['purchase_roles']['image_pass'])
        await user.remove_roles(image_pass, reason="Removed Image Pass role.")
        await ctx.interaction.response.send_message(embed=utils.Embed(color=0xc77f22, desc=f"# {user} is now image pass banned."))
        await self.discord_log.send(embed=utils.Embed(color=0xc77f22, desc=f"# {user.name} has been image banned.", thumbnail=member.avatar.url))







    @utils.is_mod_staff()
    @command(
        aliases=['pr'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="User whose messages you want to delete.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
                ApplicationCommandOption(
                    name="amount",
                    description="Amount of messages you want to delete.",
                    type=ApplicationCommandOptionType.integer,
                    required=False,
                ),
            ],
        )
    )
    async def prune(self, ctx, user:User, amount: int = 100):
        """Purges message from a specific user!"""
        check = lambda m: m.author.id == user.id

        # ! Add max amount
        if amount > 250:
            return await ctx.interaction.response.send_message(f"**250 is the maximum amount of messages.**")

        # ! Report and log the purging!
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.interaction.response.send_message(embed=utils.Embed(color=randint(1, 0xffffff), desc=f"# Deleted {len(removed)} messages!")
        )


    @utils.is_mod_staff()
    @command(
        aliases=['pu'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="amount",
                    description="Amount of messages you want to delete.",
                    type=ApplicationCommandOptionType.integer,
                    required=False,
                ),
            ],
        )
    )
    async def purge(self, ctx, amount: int = 100):
        """Purges the given amount of messages from the channel."""
        check = lambda m: True

        # ! Add max amount
        if amount > 250:
            return await ctx.interaction.response.send_message(f"**250 is the maximum amount of messages.**")

        # ! Report and log the purging!
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.interaction.response.send_message(
            embed=utils.Embed(desc=f"# Deleted {len(removed)} messages!"))
        await self.message_log.send(embed=utils.Embed(color=0xc74822, desc=f"# <@{ctx.author.id}> purged {amount} messages from <#{ctx.channel.id}>!"))


    @utils.is_mod_staff()
    @command(
        aliases=['cl'],
        application_command_meta=ApplicationCommandMeta(),
    )
    async def clean(self, ctx):
        """Clears the bot's messages!"""
        check = lambda m: m.author.id == self.bot.config['bot_id'] or m.id == ctx.message.id or m.content.startswith(
            self.bot.config['prefix'])
        await ctx.channel.purge(check=check)


def setup(bot):
    x = Staff_Actions(bot)
    bot.add_cog(x)
