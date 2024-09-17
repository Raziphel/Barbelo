# Discord
from discord import User, ApplicationCommandOption, ApplicationCommandOptionType, Member
from discord.ext.commands import command, cooldown, BucketType, Cog, ApplicationCommandMeta

# Utils
import utils
from math import floor


class Payment(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  # ! The members log
    def coin_logs(self):
        return self.bot.get_channel(self.bot.config['channels']['coin_logs']) 

    @cooldown(1, 30, BucketType.user)
    @command(
        aliases=['send'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="recipient",
                    description="The user you want to send coins to.",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="amount",
                    description="The amount of coins you'd like to send.",
                    type=ApplicationCommandOptionType.integer,
                    required=True,
                ),
            ],
        ),
    )
    async def pay(self, ctx, recipient: Member = None, amount: int = 0):
        """Send coins to another member (With a tax)."""
        coin_e = self.bot.config['emojis']['coin']

        #? Check if the recipient is the same as the user.
        if recipient == ctx.author:
            return await ctx.interaction.response.send_message(embed=utils.Embed(description=f"{ctx.author.name} You can't pay yourself coins! stupid..."))

        if amount <= 1000:
            return await ctx.interaction.response.send_message(embed=utils.Embed(description=f"{ctx.author.name} Has to be more than 1,000!"))

        #? Check if the user has enough coins.
        c = utils.Currency.get(ctx.author.id)
        if amount > (c.coins - amount*0.08):
            return await ctx.interaction.response.send_message(embed=utils.Embed(description=f"{recipient.mention} you don't have that many coins.  (Could be due to taxes)"))

        tax = await utils.CoinFunctions.pay_user(payer=ctx.author, receiver=recipient, amount=amount)

        await ctx.interaction.response.send_message(embed=utils.Embed(description=f"**{ctx.author} sent {coin_e} {floor(amount):,}x to {recipient}!**\n*Taxes: {floor(tax):,}*"))

        await self.coin_logs.send(f"**{ctx.author.name}** payed **{coin_e} {amount}x** to **{recipient.name}**!")


def setup(bot):
    x = Payment(bot)
    bot.add_cog(x)