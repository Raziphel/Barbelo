
#* Discord
import discord
from discord.ext.commands import command, Cog, ApplicationCommandMeta, cooldown, BucketType
from discord import Member, Message, User, ApplicationCommandOption, ApplicationCommandOptionType


import utils



class profile(Cog):
    def __init__(self, bot):
        self.bot = bot



    @command(
        aliases=['coin'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user you'd like to see the coins of!",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        ),
    )
    async def coins(self, ctx, user:User=None):
        '''Quick Check Coins'''
        if not user:
            user = ctx.author

        c = utils.Coins.get(user.id)
        emoji = self.bot.config['emojis']['coin_emoji']

        await ctx.interaction.response.send_message(content=f"**Showing <@{user.id}>'s Coins Stats:**", embed=utils.Embed(desc=f"**{emoji}{c.coins:,}x in there pockets!**\n\nEarned: {emoji}{c.earned:,}x\nSpent: {emoji}{c.spent:,}x\nTaxed: {emoji}{c.taxed:,}x\nLost: {emoji}{c.lost:,}x\nStolen: {emoji}{c.stolen:,}x\nGifted: {emoji}{c.gifted:,}x\nGiven: {emoji}{c.given:,}x\nBanked: {emoji}{c.banked:,}x"))





    @cooldown(1, 5, BucketType.user)
    @command(aliases=['color', 'Color', 'Setcolor', 'SetColor'],
            application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="colour",
                    description="the color you are wanting.",
                    type=ApplicationCommandOptionType.string,
                    required=False
                    )
                ],
            ),
        )
    async def setcolor(self, ctx, colour=None):
        '''Sets your user color'''

        if colour == None:
            file = discord.File('config/lists/colors.py', filename='config/lists/colors.py')
            await ctx.interaction.response.send_message(f"**Heres a list of colors you can use!**", file=file)
            return

        colour_value = utils.Colors.get(colour.lower())
        tr = utils.Tracking.get(ctx.author.id)

        if colour_value == None:
            try:
                colour_value = int(colour.strip('#'), 16)
            except ValueError:
                await ctx.interaction.response.send_message(embed=utils.Embed(title="Incorrect colour usage!"))
                return

        tr.color = colour_value
        async with self.bot.database() as db:
            await tr.save(db)

        await ctx.interaction.response.send_message(embed=utils.Embed(title="Your color setting has been set!", user=ctx.author))



def setup(bot):
    x = profile(bot)
    bot.add_cog(x)
