
#* Discord
from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

# * Additions
from math import floor

import utils



class rules_handler(Cog):
    def __init__(self, bot):
        self.bot = bot



    @Cog.listener('on_ready') #! ---> Server Rules
    async def rules(self):

        embed1=Embed(description=f"# Server Etiquette\n⦁ Try to maintain the natural flow of a conversation already in progress. Do not spam, post irrelevant images or purposely disrupt the chat in any way.\n⦁ Avoid sending repeating messages as well as repeated characters, emojis or phrases.\n⦁ Try to keep your messages together. Avoid breaking your paragraphs up into multiple lines and sending messages too quickly.\n⦁ Keep roleplay short and casual. The occasional head-pat, hug or high-five is fine, but limit non-conversation to only one or two messages.\n⦁ This is an English-speaking server. Please communicate in a way our members and staff can understand while participating in this server.", color=0x80F75C)

        embed2=Embed(description=f"# 2. Respect\nExcessively argumentative, rude, dismissive, or aggressive members will be removed. We will not tolerate any instances of offensive behaviour towards anyone, nor any occurrences of racism, homophobia, transphobia or other types of discriminatory language. Jokes about these topics are equally unwelcome. Personal arguments or conversations between members should be taken to direct messages if both users wish to continue, rather than affecting the atmosphere/mood/feeling of the chat.", color=0x80F75C)

        embed3=Embed(description=f"# 3. Mental Illness\nThis includes jokes and discussing methods of harm. We care about the well-being of all our members; however, this chat is not a suitable method of mental care therapy. Instead, if you or somebody you know needs help, please seek out trained professionals for appropriate care. Resources relating to these issues can be found [Here](https://www.ispn-psych.org/mental-health-links).\n\n This rule isn't included in an attempt to deny people an emotional outlet, but instead to protect those members from malicious users who might try to convince them to harm themselves and to protect them from armchair psychologists who may make things worse.", color=0x80F75C)

        embed4=Embed(description=f"# 4. Staff Decisions\nIf any issue comes up, please ping the appropriate staff for assistance. Please do not attempt to resolve issues yourself. Staff's decisions and actions should be respected by all users; however users may contact the team for additional information, clarification or to appeal. If you have any issues with a particular staff's actions please take it to an <@&1104988250478743572> or <@&1109654196942282793> privately.\n\nIn the case of emergencies or issues that require immediate attention you can:\nPing us using <@&1068389119195107378> Please do not use this for non-emergencies.\n(Secret code for verification is Baphomet)", color=0x80F75C)

        embed5=Embed(description=f"# 5. Advertising\nAdvertisements to other groups or Discord servers are not allowed without prior staff approval. Members seeking to advertise commissions or other products must do so in the art sectioned channels. Advertisements should not include any NSFW or otherwise unsuitable content. We consider raffles, or anything which requires following, liking, retweeting, and so forth, as advertising.\n\nChoosing to DM any member of the server only to try and advertise will result in an instant ban, especially if you are a low level member.", color=0x80F75C)

        embed6=Embed(description=f"# 6. Politics\nPolitical topics may be discussed, but must be held within the discussions channels (<#{self.bot.config['channels']['politics']}>⁠). Please try to avoid any heated political discussions. This includes, but is not limited to, inflammatory remarks, stances or controversial topics, takes or media. Political imagery or references are also not suitable for inclusion in profile pictures, nicknames or emojis. This ranges from Communist and Fascist symbolism, to modern day mainstream politics and political movements. Keep rule #2 in mind and treat each other with respect during discourse.", color=0x80F75C)

        embed7=Embed(description=f"# 7. NSFW Content\nNSFW Content is only allowed channels that are specifically marked as NSFW unless stated otherwise.\n⦁ All NSFW content should only be ART!\n⦁ Absolutely no real life NSFW images is allowed!\n⦁ Any extreme fetish, loli or anything against Discord TOS is NOT allowed!\n⦁ All NSFW content is subject to deletion and moderation by staff discretion.\nWe go to extreme links to make sure ONLY adults have access to NSFW areas, there is absolutely no exceptions to these rules for anyone!", color=0x80F75C)

        embed8=Embed(description=f"# 8. Alt Accounts\nDue to potential user abuse, users are not allowed to have alts within the server. If a user is found with an alt, the alt(s) and main account will be removed. Please keep any and all alts out of the server.", color=0x80F75C)

        embed9=Embed(description=f"# 9. Verification\n**Please click the ✔ reaction to begin the verification process,**", color=0x80F75C)


        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules = {}
        for i in range(1, 10):
            rules[i] = await ch.fetch_message(self.bot.config['rules_messages'][str(i)])

        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9]

        for i, rule in rules.items():
            await rule.edit(content="", embed=embeds[i-1])

        # rules1 = await ch.fetch_message(self.bot.config['rules_messages']['1']) 
        # rules2 = await ch.fetch_message(self.bot.config['rules_messages']['2'])
        # rules3 = await ch.fetch_message(self.bot.config['rules_messages']['3'])
        # rules4 = await ch.fetch_message(self.bot.config['rules_messages']['4'])
        # rules5 = await ch.fetch_message(self.bot.config['rules_messages']['5'])
        # rules6 = await ch.fetch_message(self.bot.config['rules_messages']['6'])
        # rules7 = await ch.fetch_message(self.bot.config['rules_messages']['7'])
        # rules8 = await ch.fetch_message(self.bot.config['rules_messages']['8'])
        # rules8 = await ch.fetch_message(self.bot.config['rules_messages']['9'])


        # await rules1.edit(content=f" ", embed=embed1)
        # await rules2.edit(content=f" ", embed=embed2)
        # await rules3.edit(content=f" ", embed=embed3)
        # await rules4.edit(content=f" ", embed=embed4)
        # await rules5.edit(content=f" ", embed=embed5)
        # await rules6.edit(content=f" ", embed=embed6)
        # await rules7.edit(content=f" ", embed=embed7)
        # await rules8.edit(content=f" ", embed=embed8)
        # await rules9.edit(content=f" ", embed=embed9)






def setup(bot):
    x = rules_handler(bot)
    bot.add_cog(x)