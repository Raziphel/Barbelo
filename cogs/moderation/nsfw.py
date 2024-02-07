
#* Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, Message, User, ApplicationCommandOption, ApplicationCommandOptionType
from discord.ext.commands import ApplicationCommandMeta

import utils

class nsfw(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #+ The Members Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 


    @utils.is_mod_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be revoked NSFW access!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
            ],
        ),
    )
    async def notnsfw(self, ctx, user:Member):
        '''Removes nsfw access from a user!'''

        #+ Get some varibles!
        mod = utils.Moderation.get(user.id)
        nsfw_adult = utils.DiscordGet(ctx.guild.roles, id=self.bot.config['age_roles']['nsfw_adult'])
        adult = utils.DiscordGet(ctx.guild.roles, id=self.bot.config['age_roles']['adult'])


        try: #* Removes 18+ role if exists!
            await user.remove_roles(nsfw_adult)
            await user.remove_roles(adult)
        except: pass

        #* Add the underage role and update nsfw!
        underage = utils.DiscordGet(user.guild.roles, id=self.bot.config['age_roles']['underage'])
        await user.add_roles(underage)

        mod.child = True
        mod.adult = False
        async with self.bot.database() as db:
            await mod.save(db)

        #* Log the action!
        await self.discord_log.send(embed=utils.Embed(color=0xc77f22, title=f"NSFW Restricted", desc=f"{user.name} was nsfw restricted"))
        await ctx.send(embed=utils.Embed(color=0xc77f22, title=f"{user.mention}, has been NSFW restricted!"))


    @utils.is_mod_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be given NSFW access!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
            ],
        ),
    )
    async def nsfw(self, ctx, user:Member):
        '''Gives nsfw access to a user!'''

        #+ Get some varibles!
        mod = utils.Moderation.get(user.id)
        nsfw_adult = utils.DiscordGet(ctx.guild.roles, id=self.bot.config['age_roles']['nsfw_adult'])
        underage = utils.DiscordGet(user.guild.roles, id=self.bot.config['age_roles']['underage'])

        try: #* Removes underage role if exists!
            await user.remove_roles(underage)
        except: pass

        #* Add the underage role and update nsfw!
        await user.add_roles(nsfw_adult)

        mod.child = False
        mod.adult = True
        async with self.bot.database() as db:
            await mod.save(db)

        #* Log the action!
        await self.discord_log.send(embed=utils.Embed(color=0x339c2a, title=f"NSFW Allowed", desc=f"{user.name} was nsfw unrestricted and given."))
        await ctx.send(embed=utils.Embed(color=0x339c2a, title=f"{user.mention}, has been NSFW unrestricted!"))




def setup(bot):
    x = nsfw(bot)
    bot.add_cog(x)