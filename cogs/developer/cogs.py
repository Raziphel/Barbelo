import os

#* Discord
from discord.ext.commands import command, Cog, cog
from glob import glob

import utils


class Cogs(Cog):
    def __init__(self, bot):
        self.bot = bot


    @utils.is_dev()
    @command(aliases=['rld'])
    async def reload(self, ctx):
        """Reloads all cogs"""
        extensions = [i.replace(os.sep, '.')[:-3] for i in glob("Cogs/*/[!_]*.py")]
        for extension in extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                print(f"Failed to load {extension}")
                await ctx.send(embed=utils.DevEmbed(title=f"Reload Cog Command Failed", desc=f"The cog: `{cog}` couldn't be reloaded.  Error was sent to console logs."))
                raise e
        await ctx.send(embed=utils.DevEmbed(title=f"Cogs Reloaded!", desc=f"All cogs were successfully reloaded!"))


    @utils.is_dev()
    @command(aliases=['ld'])
    async def load(self, ctx, cog:str):
        """Loads a cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(embed=utils.DevEmbed(title=f"Load Cog Command Successful", desc=f"The cog: `{cog}` was loaded."))
        except Exception as e:
            await ctx.send(embed=utils.DevEmbed(title=f"Load Cog Command Failed", desc=f"The cog: `{cog}` couldn't be loaded."))
            raise e


    @utils.is_dev()
    @command(aliases=['uld'])
    async def unload(self, ctx, cog:str):
        """Unloads a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(embed=utils.DevEmbed(title=f"Unload Cog Command Successful", desc=f"The cog: `{cog}` was unloaded."))
        except Exception as e:
            await ctx.send(embed=utils.DevEmbed(title=f"Unload Cog Command Failed", desc=f"The cog: `{cog}` couldn't be unloaded.",))
            raise e


def setup(bot):
    x = Cogs(bot)
    bot.add_cog(x)