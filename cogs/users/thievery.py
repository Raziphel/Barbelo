from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter, ApplicationCommandMeta
from discord import Member, Message, User, Game, Embed, TextChannel, Role, RawReactionActionEvent, ApplicationCommandOption, ApplicationCommandOptionType

#* Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils



class thievery(Cog):
    def __init__(self, bot):
        self.bot = bot



    @property  #! The currency logs
    def gem_logs(self):
        return self.bot.get_channel(self.bot.config['logs']['gems'])




    @command(application_command_meta=ApplicationCommandMeta())
    async def larceny(self, ctx):
        '''
        Enables or disabled the ability to steal.
        '''
        skills = utils.Skills.get(ctx.author.id)

        if (skills.larceny_stamp + timedelta(hours=2)) >= dt.utcnow():
            tf = skills.larceny_stamp + timedelta(hours=2)
            t = dt(1, 1, 1) + (tf - dt.utcnow())
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"You can change your larceny setting in:\n**{t.hour} hours and {t.minute} minutes!**", user=ctx.author))

        
        if skills.larceny == False:
            skills.larceny = True
            await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"# Larceny Enabled!\nYou can now steal and be stolen from!", user=ctx.author))

        elif skills.larceny == True:
            skills.larceny = False
            await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"# Larceny Disabled!\nYou can no longer steal or be stolen from!", user=ctx.author))

        skills.larceny_stamp = dt.utcnow()

        async with self.bot.database() as db:
            await skills.save(db)








    @command(        
        aliases=['yoink'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user you would like to steal from!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
            ],
        ),
    )
    async def steal(self, ctx, user:Member=None):
        '''
        Use your gloves to steal from other users!!
        '''

        #! Define Varibles
        amount = choice([5, 10, 15, 20, 25])
        gem_type = choice(['diamond', 'ruby', 'sapphire'])
        g = utils.Gems.get(ctx.author.id)
        og = utils.Gems.get(user.id)
        skills = utils.Skills.get(ctx.author.id)
        oskills = utils.Skills.get(user.id)


        #? Check everything!
        if user.id == self.bot.user.id:
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"You can't steal from the master of thiefs!", user=ctx.author))

        if user.id == ctx.author.id:
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"You can't steal from yourself!", user=ctx.author))

        if skills.thievery == False:
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"You are not capable of stealing until you buy it from the shop!", user=ctx.author))

        if skills.larceny == False:
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"You have not enabled `/larceny` to be able to steal!", user=ctx.author))

        if oskills.larceny == False:
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"{user.mention} has not enabled larceny!", user=ctx.author))

        if (skills.larceny_stamp + timedelta(hours=2)) >= dt.utcnow():
            tf = skills.larceny_stamp + timedelta(hours=2)
            t = dt(1, 1, 1) + (tf - dt.utcnow())
            return await ctx.interaction.response.send_message(embed=utils.Embed(desc=f"You are not capable of stealing for another:\n**{t.hour} hours and {t.minute} minutes!**", user=ctx.author))

        gems_stolen = None
        skills.larceny_stamp = dt.utcnow()

        diamonds = 0
        rubys = 0
        sapphires = 0

        if gem_type == 'diamond':
            og.diamond -= amount
            g.diamond += amount
            diamonds = amount

        elif gem_type == 'ruby':
            og.ruby -= amount
            g.ruby += amount
            rubys = amount

        elif gem_type == 'sapphire':
            og.sapphire -= amount
            g.sapphire += amount
            sapphires = amount

        gem_string = await utils.GemFunctions.gems_to_text(diamonds=diamonds, rubys=rubys, sapphires=sapphires)

        await ctx.interaction.response.send_message(
                content=f"{user.mention}", embed=utils.Embed(title=f"🧤 Gems Stolen 🧤", desc=f"**{ctx.author.name}** Stole gems from **{user.name}** and they gained {gem_string}", user=ctx.author))
        await self.gem_logs.send(f"**{ctx.author.name}** Stole gems from **{user.name}** and they gained {gem_string}")


        async with self.bot.database() as db:
            await skills.save(db)
            await g.save(db)
            await og.save(db)




def setup(bot):
    x = thievery(bot)
    bot.add_cog(x)