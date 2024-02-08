
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



class rules_handler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #+ The Server Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 



    @Cog.listener('on_ready') #! ---> Server Rules
    async def rules(self):

        embed1=Embed(description=f"# Server Etiquette\n⦁ Try to maintain the natural flow of a conversation already in progress. Do not spam, post irrelevant images or purposely disrupt the chat in any way.\n⦁ Avoid sending repeating messages as well as repeated characters, emojis or phrases.\n⦁ Try to keep your messages together. Avoid breaking your paragraphs up into multiple lines and sending messages too quickly.\n⦁ Keep roleplay short and casual. The occasional head-pat, hug or high-five is fine, but limit non-conversation to only one or two messages.\n⦁ This is an English-speaking server. Please communicate in a way our members and staff can understand while participating in this server.", color=0x80F75C)

        embed2=Embed(description=f"# 2. Respect\nExcessively argumentative, rude, dismissive, or aggressive members will be removed. We will not tolerate any instances of offensive behaviour towards anyone, nor any occurrences of racism, homophobia, transphobia or other types of discriminatory language. Jokes about these topics are equally unwelcome. Personal arguments or conversations between members should be taken to direct messages if both users wish to continue, rather than affecting the atmosphere/mood/feeling of the chat.", color=0x80F75C)

        embed3=Embed(description=f"# 3. Mental Illness\nThis includes jokes and discussing methods of harm. We care about the well-being of all our members; however, this chat is not a suitable method of mental care therapy. Instead, if you or somebody you know needs help, please seek out trained professionals for appropriate care. Resources relating to these issues can be found [Here](https://www.ispn-psych.org/mental-health-links).\n\n This rule isn't included in an attempt to deny people an emotional outlet, but instead to protect those members from malicious users who might try to convince them to harm themselves and to protect them from armchair psychologists who may make things worse.", color=0x80F75C)

        embed4=Embed(description=f"# 4. Staff Decisions\nIf any issue comes up, please ping the appropriate staff for assistance. Please do not attempt to resolve issues yourself. Staff's decisions and actions should be respected by all users; however users may contact the team for additional information, clarification or to appeal. If you have any issues with a particular staff's actions please take it to an <@&1104988250478743572> or <@&1109654196942282793> privately.\n\nIn the case of emergencies or issues that require immediate attention you can:\nPing us using <@&1068389119195107378> Please do not use this for non-emergencies.\n(Secret phrase for verification is Baphomet)", color=0x80F75C)

        embed5=Embed(description=f"# 5. Advertising\nAdvertisements to other groups or Discord servers are not allowed without prior staff approval. Members seeking to advertise commissions or other products must do so in the art sectioned channels. Advertisements should not include any NSFW or otherwise unsuitable content. We consider raffles, or anything which requires following, liking, retweeting, and so forth, as advertising.\n\nChoosing to DM any member of the server only to try and advertise will result in an instant ban, especially if you are a low level member.", color=0x80F75C)

        embed6=Embed(description=f"# 6. Politics\nPolitical topics may be discussed, but must be held within the discussions channels (<#{self.bot.config['channels']['politics']}>⁠). Please try to avoid any heated political discussions. This includes, but is not limited to, inflammatory remarks, stances or controversial topics, takes or media. Political imagery or references are also not suitable for inclusion in profile pictures, nicknames or emojis. This ranges from Communist and Fascist symbolism, to modern day mainstream politics and political movements. Keep rule #2 in mind and treat each other with respect during discourse.", color=0x80F75C)

        embed7=Embed(description=f"# 7. NSFW Content\nNSFW Content is only allowed channels that are specifically marked as NSFW unless stated otherwise.\n⦁ All NSFW content should only be ART!\n⦁ Absolutely no real life NSFW images is allowed!\n⦁ Any extreme fetish, loli or anything against Discord TOS is NOT allowed!\n⦁ All NSFW content is subject to deletion and moderation by staff discretion.\nWe go to extreme links to make sure ONLY adults have access to NSFW areas, there is absolutely no exceptions to these rules for anyone!", color=0x80F75C)

        embed8=Embed(description=f"# 8. Alt Accounts\nDue to potential user abuse, users are not allowed to have alts within the server. If a user is found with an alt, the alt(s) and main account will be removed. Please keep any and all alts out of the server.", color=0x80F75C)

        embed9=Embed(description=f"# 9. Verification\n**Please click the ✅ reaction to begin the verification process.**\n*The bot must be able to message you!*\n\n`WARNING: You must get these answers correct or you will be kicked.`", color=0x80F75C)


        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules = {}
        for i in range(1, 10):
            rules[i] = await ch.fetch_message(self.bot.config['rules_messages'][str(i)])

        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9]

        for i, rule in rules.items():
            await rule.edit(content="", embed=embeds[i-1])





    @Cog.listener('on_raw_reaction_add')
    async def verify(self, payload:RawReactionActionEvent):
            '''Send verification message~!'''

            # See if I need to deal with it
            if payload.channel_id != self.bot.config['channels']['rules']: #? Verification Channel
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            # See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji.id
        
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            if emoji == "✅":
                await self.verification(author=member)

            # Check to see total reactions on the message
            channel_id = payload.channel_id
            channel = self.bot.get_channel(channel_id)
            async for message in channel.history():
                if message.id == payload.message_id:
                    break 
            if message.id != payload.message_id:
                return  # Couldn't find message in channel history

            # See total reactions
            emoji = [i.emoji for i in message.reactions]
            if sum([i.count for i in message.reactions]) > 5000:
                await message.clear_reactions()
            for e in emoji:
                await message.add_reaction(e)





    async def verification(self, author):
        '''Sends a verification application!'''


        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild

        async def get_input(prompt: str, timeout: float = 300.0, max_length: Optional[int] = 50):
            '''Gets users responses and checks them'''
            await author.send(embed=utils.Embed(color=randint(1, 0xffffff), desc=prompt))

            async def get_response():
                ''''Waits for users responses'''
                msg = await self.bot.wait_for('message', check=lambda m: m.author.id == author.id and not m.guild, timeout=timeout)

                if 'cancel' == msg.content.lower():
                    raise VerificationCancelled

                return msg

            message = await get_response()

            if max_length is not None:
                while len(message.content) > max_length:
                    await author.send(f"Sorry, but the value you've responded with is too long. Please keep it within {max_length} characters.")
                    message = await get_response()

            return message

        try:
            invited_answer = await get_input(f"Where did you recieve an invintation to {guild.name} from?")

            age_answer = await get_input("How old are you?")
            age_answer =get_only_numbers(age_answer.content)

            mod = utils.Moderation.get(author.id)
            if age_answer < 18:
                mod.child = True

            color = await get_input("What's your favourite colour? (Say a color name or a hex code)")
            colour_value = utils.Colors.get(color.content.lower()) 
            if colour_value == None:
                try:
                    colour_value = int(color.content.strip('#'), 16)
                except ValueError:
                    pass
            t = utils.Tracking.get(author.id)
            t.color = colour_value
            async with self.bot.database() as db:
                await t.save(db)
                await mod.save(db)

            if color is None:
                color = 0x0
                await author.send('Invalid color specified!\nSetting to default color.')

            verify_answer = await get_input("What is the secret phrase found in the rules?\n**WARNING** putting anything but the phrase perfectly will result in being kicked from the server.")

            msg = f"How they were invited: {invited_answer.content}\nAge given: {age_answer.content}\nPhrase Given: {verify_answer.content}"
            msg = await self.discord_log.send(embed=utils.Embed(footer=f"Verification", message=msg, color=t.color, author=author, image=author.avatar_url))

            if verify_answer.content.lower() == "baphomet" and age > 12:
                embed2=Embed(description="**You have been accepted!**")
                await author.send(embed=embed2)
                await utils.UserFunctions.verify_user(author)
            else:
                embed2=Embed(description="**You have been denied!**")
                await author.send(embed=embed2)
                await self.bot.kick(author)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except VerificationCancelled:
            await author.send('Aborting Verification!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')






def setup(bot):
    x = rules_handler(bot)
    bot.add_cog(x)