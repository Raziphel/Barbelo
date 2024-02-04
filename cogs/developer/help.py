# Discord
from random import randint

from discord import Embed
from discord.ext.commands import command, Cog, Group, ApplicationCommandMeta


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.original_help = bot.get_command('help')
        bot.remove_command('help')

    def cog_unload(self):
        self.bot.add_comand(self.original_help)

    async def cog_command_error(self, ctx, error):
        raise error

    @command(
        name='help',
        aliases=['commands'],
        hidden=True,
        application_command_meta=ApplicationCommandMeta(),
    )
    async def help(self, ctx, *, command_name: str = None):
        """Gives you the new help command uwu"""

        #* Get all the cogs
        if not command_name:
            cogs = self.bot.cogs.values()
            cog_commands = [cog.get_commands() for cog in cogs]
        else:
            command = self.bot
            for i in command_name.split():
                command = command.get_command(i)
                if not command:
                    await ctx.send(f"The command `{command_name}` could not be found.")
                    return
            base_command = command
            if isinstance(base_command, Group):
                cog_commands = [list(set(command.walk_commands()))]
            else:
                cog_commands = []

        #? See which the user can run
        runnable_commands = []
        for cog in cog_commands:
            runnable_cog = []
            for command in cog:
                runnable = command.hidden == False and command.enabled == True
                if runnable:
                    runnable_cog.append(command)
            runnable_cog.sort(key=lambda x: x.name)
            if len(runnable_cog) > 0:
                runnable_commands.append(runnable_cog)

        #? Sort cogs list based on name
        runnable_commands.sort(key=lambda x: x[0].cog_name)

        #* Make an embed
        help_embed = Embed()
        help_embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar.url)
        help_embed.colour = randint(1, 0xffffff)

        #* Add commands to it
        if command_name:
            help_embed.add_field(name=f"{ctx.prefix}{base_command.qualified_name}", value=f"{base_command.help}")
        for cog_commands in runnable_commands:
            value = '\n'.join(
                [f"**{ctx.prefix}{command.qualified_name}** - *{command.short_doc}*" for command in cog_commands])
            help_embed.add_field(
                name=cog_commands[0].cog_name,
                value=value,
                inline=False
            )

        #! Send it to the user
        try:
            await ctx.author.send(embed=help_embed)
            if ctx.guild:
                await ctx.send('I\'ve sent you a DM with a list of commands!')
        except Exception:
            await ctx.send("I am not able to DM you a list of commands.\nYou will need to change your privacy settings.")


def setup(bot):
    x = Help(bot)
    bot.add_cog(x)
