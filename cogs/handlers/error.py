
#* Discord
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument, CommandNotFound, CommandOnCooldown, MissingPermissions, IsNotSlashCommand
#* Utils
import utils
#* Additions
from asyncio import sleep



class error_handler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Handles any errors the bot runs into'''

        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Ya don't have the right Server Permission!"))
            pass
        elif isinstance(error, BadArgument):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Ya gave Incorrect Command Arguments!?"))
            pass
        elif isinstance(error, utils.InDmsCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"This command can only be ran in my Dms!"))
            pass
        elif isinstance(error, utils.UserCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Only someone special can run this command!"))
            pass
        elif isinstance(error, utils.DevCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Only the Bot Developer can run this command!"))
            pass
        elif isinstance(error, utils.GuildCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"This isn't the right Discord Server for this command."))
            pass
        elif isinstance(error, utils.NSFWCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"An NSFW Error Occured."))
            pass
        elif isinstance(error, utils.ModStaffCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Only a Moderator can run this command!"))
            pass
        elif isinstance(error, utils.AdminStaffCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Only an Administrator can run this command!"))
            pass
        else: 
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"Something unexpected happened?"))
            pass

        if ctx.author.id in self.bot.config['developers'].values():
            await ctx.author.send(f"Command failed - `{error!s}`;")

        await sleep(4)
        try:
            await msg.delete()
            await ctx.message.delete()
        except: pass

def setup(bot):
    x = error_handler(bot)
    bot.add_cog(x)
