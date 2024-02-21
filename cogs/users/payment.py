# Discord
from discord.ext.commands import command, cooldown, ApplicationCommandMeta, ApplicationCommandOption, BucketType, Cog
from discord import Message, User
# Utils
import utils


class TooPoor(BaseException):
    pass


class payment(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #! The currency logs
    def gem_logs(self):
        return self.bot.get_channel(self.bot.config['logs']['gems'])


    @cooldown(1, 30, BucketType.user)
    @command(
        aliases=['send'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="recipient",
                    description="The user you want to send gems to.",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="amount",
                    description="The amount of gems you'd like to send.",
                    type=ApplicationCommandOptionType.integer,
                    required=True,
                ),
            ],
        ),
    )
    @command(aliases=['send'])
    async def pay(self, ctx, receiver:User=None, gems:int=0):
        '''
        sending payemnts to other members
        '''
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        g = utils.Currency.get(ctx.author.id)
        g_r = utils.Currency.get(receiver.id)

        if receiver == ctx.author:
            await ctx.send(embed=utils.Embed(desc=f"# {ctx.author.mention} You can't pay yourself gems!", user=ctx.author))
            return
        if gems <= 0 or gems > 99:
            await ctx.send(embed=utils.Embed(desc=f"# {ctx.author.mention} Has to be more than 0 and less than 99 gems!", user=ctx.author))
            return

        embed = utils.Embed(desc=f"# Click the emote for currency type! ",user=ctx.author)
        msg = await ctx.send(embed=embed)

        # adds the reactions
        await msg.add_reaction(self.bot.config['gem_emoji']['diamond'])
        await msg.add_reaction(self.bot.config['gem_emoji']['ruby'])
        await msg.add_reaction(self.bot.config['gem_emoji']['sapphire'])
        await msg.add_reaction(self.bot.config['gem_emoji']['amethyst'])

        try:

            # Watches for the reactions
            check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and str(x.emoji) in [self.bot.config['gem_emoji']['diamond'], self.bot.config['gem_emoji']['ruby'], self.bot.config['gem_emoji']['sapphire'], self.bot.config['gem_emoji']['amethyst']]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if str(r.emoji) == self.bot.config['gem_emoji']['diamond']:
                purchased = await utils.GemFunctions.payment(user=ctx.author, gem=self.bot.config['gem_emoji']['diamond'], amount=gems)
                if purchased == False:
                    raise TooPoor

            if str(r.emoji) == self.bot.config['gem_emoji']['ruby']:
                purchased = await utils.GemFunctions.payment(user=ctx.author, gem=self.bot.config['gem_emoji']['ruby'], amount=gems)
                if purchased == False:
                    raise TooPoor

            if str(r.emoji) == self.bot.config['gem_emoji']['sapphire']:
                purchased = await utils.GemFunctions.payment(user=ctx.author, gem=self.bot.config['gem_emoji']['sapphire'], amount=gems)
                if purchased == False:
                    raise TooPoor

            if str(r.emoji) == self.bot.config['gem_emoji']['amethyst']:
                purchased = await utils.GemFunctions.payment(user=ctx.author, gem=self.bot.config['gem_emoji']['amethyst'], amount=gems)
                if purchased == False:
                    raise TooPoor


        except TooPoor:
            await ctx.send(f'# {ctx.author.mention} Payment denied. You would go in debt stupid!!!')
            return

        #! Always update after paying!
        await utils.GemFunctions.update(user=ctx.author)
        await utils.GemFunctions.update(user=receiver)

        async with self.bot.database() as db:
            await c.save(db)
            await c_r.save(db)

        await msg.delete()
        await ctx.send(embed=utils.Embed(tuser=ctx.author, desc=f"# {gems} {str(r.emoji)} was sent to {receiver}!"))

        await self.gem_logs.send(embed=utils.Embed(user=ctx.author, desc=f"# {ctx.author} payed {gems} {str(r.emoji)} was sent to {receiver}!"))





def setup(bot):
    x = payment(bot)
    bot.add_cog(x)