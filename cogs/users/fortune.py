# Discord
from discord.ext.commands import command, Cog, ApplicationCommandMeta, cooldown, BucketType
from discord import Member, User, ApplicationCommandOption, ApplicationCommandOptionType
# Additions
from random import choice
from time import monotonic

# Utils
import utils

class fortune(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.YesorNo = ([
            "Yeah, why not...",
            "Yes, but that's gross!",
            "No. Your a loser! >;c",
            "I can't answer stupidity.",
            "Yeah, but thats really stupid!",
            "No, you nasty furry~",
            "Eww wtf. Hell no!",
            "Only a homosexual would ask that.",
            "I was told to say No.",
            "I was told to say Yes.",
            "Wtf?  Yeah fuck no.",
            "Oh fuck.  Fuck Yes.",
            "Yeah, but you need jesus...",
            "No x100!  Thats horrible.",
            "Why ofcourse you gayfur~",
            "Yeah no.  100% not!",
            "Wow, hell no! settle down there f slur!",
            "No, thank you. But that's gross.",
            "Yeah, but your probably gonna get a disease...",
            "Are you gay? Then maybe...",
            "Yes, but you'll get cancer",
            "Yes but your lover will harass you.",
            "Oh my fucking god, yes!", 
            "Yes, but only if it's tuesday.", 
            "What are you talking about? Of course not!?",  
            "The answer is yes, but your gay af for asking.", 
            "Never going to happen! Ever!", 
            "Nope, never!", 
            "Yes, but get drunk af first!", 
            "Only if you eat ass while doing it.", 
            "Probably, yeah?",
            "Oh baby.  You better believe it.",
            "It's a high likelyhood!",
            "Yikes, how about no.",
            "Yoooooo, hell no, settle down.",
            "Omfg, yeah thats a big fat no.",
            "Wtf, yeah why not.",
            "C'mon you already know thats a no.",
            "You ask too many questions, but no.",
            "Sometimes...",
            "Without a doubt thats a no.",
            "Hell no, to the no.",
            "Yeah for sure.",
            "Shut the hell up, ofcourse.",
            "God damn it, NO."
        ])


    @command(aliases=['8ball', 'fortune', 'Ask', 'Fortune'],
            application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="question",
                    description="The question you wish to ask!",
                    type=ApplicationCommandOptionType.string,
                    required=True,
                ),
            ],
        ),
    )
    async def ask(self, ctx, question):
        '''
        Ask the bot a yes or no question.
        '''
        contents = question.split()
        total_words = len(question.split())
        response = "I don't understand that question~"

        for word in contents:
            if word.lower() in ["am", "will", "does", "should", "can", "are", "do", "is"]:
                response = choice(self.YesorNo)

        await ctx.send(embed=utils.Embed(desc=response))











def setup(bot):
    x = fortune(bot)
    bot.add_cog(x)