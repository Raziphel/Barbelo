
#* Discord
from discord.ext.commands import command, Cog
from discord import Member, PermissionOverwrite, Permissions

#*Additions
from asyncio import sleep, iscoroutine
from time import monotonic
from datetime import datetime as dt, timedelta
from random import choice
import utils
import os
import sys
import subprocess

from asyncio import iscoroutine, gather
from traceback import format_exc


class Developer(Cog):
    def __init__(self, bot):
        self.bot = bot


    @utils.is_dev()
    @command()
    async def ev(self, ctx, *, content:str):
        '''
        Runs code through Python
        '''
        try:
            ans = eval(content, globals(), locals())
        except Exception:
            await ctx.send('```py\n' + format_exc() + '```')
            return
        if iscoroutine(ans):
            ans = await ans
        await ctx.send('```py\n' + str(ans) + '```')



    @utils.is_dev()
    @command(aliases=['r'])
    async def restart(self, ctx):
        '''Restarts the bot'''  
        msg = await ctx.send(embed=utils.Embed(title=f"Restarting...", guild=ctx.guild))
        for num in range(5):
            await sleep(1)
            await msg.edit(embed=utils.Embed(title=f"Restarting in {5-num}.", guild=ctx.guild))
        await ctx.message.delete()
        await msg.delete()
        python = sys.executable
        os.execl(python, python, *sys.argv)


    @command()
    async def ping(self, ctx):
        '''Checks bot's ping'''
        await sleep(1)
        await ctx.message.delete()
        before = monotonic()
        message = await ctx.send("Pong!")
        ping = (monotonic() - before) * 1000
        users = len(set(self.bot.get_all_members()))
        servers = len(self.bot.guilds)
        await message.edit(embed=utils.Embed(desc=f"Ping:`{int(ping)}ms`\nUsers: `{users}`\nServers: `{servers}`", guild=ctx.guild))



    @utils.is_dev()
    @command()
    async def fixroles(self, ctx):
        muted = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)
        bots = utils.DiscordGet(ctx.guild.roles, id=689618590638669845)
        everyone = utils.DiscordGet(ctx.guild.roles, id=689534383878701223)
        untrusted = utils.DiscordGet(ctx.guild.roles, id=1154236618606125106)
        council = utils.DiscordGet(ctx.guild.roles, id=891793700932431942)

        verified = utils.DiscordGet(ctx.guild.roles, id=1154202953247375440)
        # for user in ctx.guild.members:
        #     if verified not in user.roles:
        #         await user.add_roles(verified, reason="verified!")

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(muted, read_messages=False, send_messages=False, add_reactions=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)
            await channel.set_permissions(bots, read_messages=True, send_messages=True, add_reactions=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True)
            await channel.set_permissions(council, manage_channels=True, manage_permissions=True)
            await channel.set_permissions(untrusted, read_messages=False, send_messages=False, add_reactions=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)

        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(muted, read_messages=None, send_messages=False, add_reactions=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, connect=False)
            # await channel.set_permissions(trusted, read_messages=True)
            await channel.set_permissions(bots, read_messages=True, send_messages=True, add_reactions=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True, connect=True)

        await ctx.send('Fixed Muted & Trust roles!')



    @utils.is_dev()
    @command()
    async def convertcoins(self, ctx):
        for member in ctx.guild.members:
            g = utils.Gems.get(member.id)
            c = utils.Currency.get(member.id)

            g.emerald = c.coins*800
            await utils.GemFunctions.update(member)
            async with self.bot.database() as db:
                await g.save(db)

        await ctx.send('All members coins have been copied over and adjusted too new currency.')




def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)