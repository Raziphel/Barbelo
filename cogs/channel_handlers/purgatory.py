
#* Discord
from discord import RawReactionActionEvent, Embed, PartialEmoji, Message, Member, DiscordException, guild
from discord.ext.commands import Cog

# * Additions
from asyncio import sleep, TimeoutError
from math import floor
from random import randint
from typing import Optional
from re import findall

import utils


class VerificationCancelled(BaseException):
    pass


def get_only_numbers(data: str):
    try:
        numbers_list = findall(r'\d+', data)
        numbers = ''.join(numbers_list)

        return int(numbers)
    except ValueError:
        return None



class purgatory(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #+ The Server Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 



    @Cog.listener('on_ready') #! ---> Server Rules
    async def rules(self):

        embed1=Embed(description=f"# __**Welcome to Esoterica**__\n", color=0xff0000)

        embed2=Embed(description=f"# 2. Respect\nExcessively argumentative, rude, dismissive, or aggressive members will be removed. We will not tolerate any instances of offensive behaviour towards anyone, nor any occurrences of racism, homophobia, transphobia or other types of discriminatory language. Jokes about these topics are equally unwelcome. Personal arguments or conversations between members should be taken to direct messages if both users wish to continue, rather than affecting the atmosphere/mood/feeling of the chat.", color=0xff0000)

        embed3=Embed(description=f"# 3. Mental Illness\nThis includes jokes and discussing methods of harm. We care about the well-being of all our members; however, this chat is not a suitable method of mental care therapy. Instead, if you or somebody you know needs help, please seek out trained professionals for appropriate care. Resources relating to these issues can be found [Here](https://www.ispn-psych.org/mental-health-links).\n\n This rule isn't included in an attempt to deny people an emotional outlet, but instead to protect those members from malicious users who might try to convince them to harm themselves and to protect them from armchair psychologists who may make things worse.", color=0xff0000)

        embed4=Embed(description=f"# 4. Staff Decisions\nIf any issue comes up, please ping the appropriate staff for assistance. Please do not attempt to resolve issues yourself. Staff's decisions and actions should be respected by all users; however users may contact the team for additional information, clarification or to appeal. If you have any issues with a particular staff's actions please take it to an <@&1104988250478743572> or <@&1109654196942282793> privately.\n\nIn the case of emergencies or issues that require immediate attention you can:\nPing us using <@&1068389119195107378> Please do not use this for non-emergencies.", color=0xBEBEBE)

        embed5=Embed(description=f"# 5. Advertising\nAdvertisements to other groups or Discord servers are not allowed without prior staff approval. Members seeking to advertise commissions or other products must do so in the art sectioned channels. Advertisements should not include any NSFW or otherwise unsuitable content. (Secret number for verification is: 33) We consider raffles, or anything which requires following, liking, retweeting, and so forth, as advertising.\n\nChoosing to DM any member of the server only to try and advertise will result in an instant ban, especially if you are a low level member.", color=0xBEBEBE)

        embed6=Embed(description=f"# 6. Politics\nPlease try to avoid any heated political discussions. This includes, but is not limited to, inflammatory remarks, stances or controversial topics, takes or media. Political imagery or references are also not suitable for inclusion in profile pictures, nicknames or emojis. This ranges from Communist and Fascist symbolism, to modern day mainstream politics and political movements. Keep rule #2 in mind and treat each other with respect during discourse.", color=0xBEBEBE)

        embed7=Embed(description=f"# 7. NSFW Content\nNSFW content is not allowed.  Do not post any sexually explicit, suggestive or excessively violent content.\n\n⦁ This applies to all forms of content. Text, images, profile pictures, statuses, etc.\n⦁ Featureless anatomy (i.e.: cartoon / barbie doll nudity) is okay.\n⦁ Images that are sexually themed or where any part of a character is featured in a sexually suggestive manner are not allowed.\n⦁ Excessive or detailed gore is not permitted.\n⦁ No questionable underage content of any kind.\n⦁ No content that could be considered to be depicting a fetish, regardless of whether some may consider it SFW.\n⦁ No alluding to or mentioning content disallowed by these rules. This includes but is not limited to phrases, imagery or external sites.\n\nIf you are unsure whether or not something is considered SFW according to this server’s rules, message a mod for clarification.", color=0x7F00FF)

        embed8=Embed(description=f"# 8. Alt Accounts\nDue to potential user abuse, users are not allowed to have alts within the server. If a user is found with an alt, the alt(s) and main account will be removed. Please keep any and all alts out of the server.", color=0x7F00FF)

        embed9=Embed(description=f"# Verification\n**Please click the ✅ reaction to begin the verification process.**\n*The bot must be able to message you!*\n\n`WARNING: You must get these answers correct or you will be kicked.`", color=0x7F00FF)


        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['welcome']) 

        welcome_banner = await ch.fetch_message(self.bot.config['welcome_messages']['banner_id']) #? 
        await welcome_banner.edit(content=f"{self.bot.config['welcome_messages']['banner_url']}", embed=embed1)

        # rules = {}
        # for i in range(2, 10):
        #     rules[i] = await ch.fetch_message(self.bot.config['rules_messages'][str(i)])

        # embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9]

        # for i, rule in rules.items():
        #     await rule.edit(content="", embed=embeds[i-1])





def setup(bot):
    x = purgatory(bot)
    bot.add_cog(x)