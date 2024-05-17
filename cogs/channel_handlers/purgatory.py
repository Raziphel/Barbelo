
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

        embed1=Embed(description=f"# __**Welcome to Esoterica**__\nEsoterica is not meant to be a normal Discord server thats sole purpose is for socializing and posting memes with your friends.\n\nHere in esoterica, members of the server are all given roles and abilities that make them capable of doing almost anything...\n\n**All members are required to accept the Esoterica - Terms of Service.**", color=0x8F00FF)

        embed2=Embed(description=f"# __**Terms of Service**__\nBy choosing to be apart of Esoterica and completing the verification process.  **__You agree to the following__:** \n\nI may be subject to \"unfair treatment\" and \"punishments\" that are automated and not brought on by any members of staff.\n\nI have fully read, understand and will uphold the rules of Esoterica.\n\nI have fully read, understand and will uphold Discord's Terms of Service.", color=0xFF0000)

        embed3=Embed(description=f"# __**Verification**__\nIf you agree to the Esoterica Terms of Service and are capable of receiving a private message then please click the ✅ reaction button to being the verification process.", color=0x8F00FF)


        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['welcome']) 

        welcome_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['welcome_id']) #? 
        await welcome_banner.edit(content=f"{self.bot.config['purgatory_banners']['welcome_url']}")

        tos_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['tos_id']) #? 
        await tos_banner.edit(content=f"{self.bot.config['purgatory_banners']['tos_url']}")

        verify_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['verify_id']) #? 
        await verify_banner.edit(content=f"{self.bot.config['purgatory_banners']['verify_url']}")

        rules = {}
        for i in range(1, 4):
            rules[i] = await ch.fetch_message(self.bot.config['welcome_messages'][str(i)])

        embeds = [embed1, embed2, embed3]

        for i, rule in rules.items():
            await rule.edit(content="", embed=embeds[i-1])







    @Cog.listener('on_ready') #! ---> Server Rules
    async def rules(self):

        embed1=Embed(description=f"# Etiquette\n🐍 **All text & voice channels are english only.**\n🐍 **No Drama.** No matter how you feel about others you can't bring it up here.\n🐍 **No Politics, No Religion.**  Only allowed in specific chats.\n🐍 **No Spamming.**  Anything that is cluttering up a chat or repetitive in VC.\n🐍 **No Self Promotion.** Unless done so in a channel deciated to self promotion.\n", color=0xff0000)

        embed2=Embed(description=f"# Respect\n🩸 **Excessively argumentative, rude, dismissive, or aggressive members will be removed.** \n🩸 We will not tolerate any instances of offensive behaviour towards anyone, nor any occurrences of **racism, homophobia, transphobia or other types of discriminatory language.**\n🩸 **Personal arguments or conversations.** This should be taken to direct messages if both users wish to continue, rather than affecting the atmosphere/mood/feeling of the chat.", color=0x8F00FF)

        embed3=Embed(description=f"# Secret Society\n🔮 **In private areas you must obey their rules and secrets.**\n🔮 **Access to these areas must be gained.** All having different requirements.\n🔮 **Designated council members** manage their respective areas.\n🔮 **Access to one area can restrict you from other areas.** ", color=0xff0000)

        embed4=Embed(description=f"# Knights, Architects, Council and Overlords\n🔱 **Overlords are owners and access to all areas.**\n🔱 **Decisions made by council are final.**\n🔱 **Knights are only helpers to council.**  Most decisions come from council.\n🔱 **Not even council have access to all areas.**\n🔱 **Council & Knights are still mortal.**\n🔱 **Architects are developers** and don't moderate.", color=0x8F00FF)

        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel


        etiquette_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['etiquette_id']) #? 
        await etiquette_banner.edit(content=f"{self.bot.config['purgatory_banners']['etiquette_url']}")

        respect_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['respect_id']) #? 
        await respect_banner.edit(content=f"{self.bot.config['purgatory_banners']['respect_url']}")

        society_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['society_id']) #? 
        await society_banner.edit(content=f"{self.bot.config['purgatory_banners']['society_url']}")

        council_banner = await ch.fetch_message(self.bot.config['purgatory_banners']['council_id']) #? 
        await council_banner.edit(content=f"{self.bot.config['purgatory_banners']['council_url']}")

        rules = {}
        for i in range(1, 5):
            rules[i] = await ch.fetch_message(self.bot.config['rules_messages'][str(i)])

        embeds = [embed1, embed2, embed3, embed4]

        for i, rule in rules.items():
            await rule.edit(content="", embed=embeds[i-1])





    @Cog.listener('on_raw_reaction_add') #! --------> verification
    async def verify(self, payload:RawReactionActionEvent):
            '''Send verification message~!'''

            # See if I need to deal with it
            if payload.channel_id != self.bot.config['channels']['welcome']: #? Verification Channel
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
                verified = utils.DiscordGet(guild.roles, id=self.bot.config['access_roles']['alive'])
                if verified not in member.roles:
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
            invited_answer = await get_input(f"Where did you recieve an invintation to Esoterica from?")

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

            verify_answer = await get_input("Do you agree to the server's TOS and plan to read the rules once verified? (Only answer is yes)")

            msg = f"How they were invited: {invited_answer.content}\nAge given: {age_answer}\nAgreed?: {verify_answer.content}"
            msg = await self.discord_log.send(embed=utils.Embed(footer=f"Verification", desc=msg, color=t.color, author=author, image=author.avatar.url))

            if verify_answer.content.lower() == "yes" and age_answer > 12:
                embed2=Embed(description="**You have been accepted!**")
                await author.send(embed=embed2)
                await utils.UserFunctions.verify_user(author)
            else:
                embed2=Embed(description="**You have been denied!**")
                await author.send(embed=embed2)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except VerificationCancelled:
            await author.send('Aborting Verification!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')












def setup(bot):
    x = purgatory(bot)
    bot.add_cog(x)