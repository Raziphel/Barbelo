
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
        guild = self.bot.get_guild(self.bot.config['guild_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(self.bot.config['rules_messages']['1']) 
        rules2 = await ch.fetch_message(self.bot.config['rules_messages']['2'])
        rules3 = await ch.fetch_message(self.bot.config['rules_messages']['3'])
        rules4 = await ch.fetch_message(self.bot.config['rules_messages']['4'])
        rules5 = await ch.fetch_message(self.bot.config['rules_messages']['5'])
        rules6 = await ch.fetch_message(self.bot.config['rules_messages']['6'])
        rules7 = await ch.fetch_message(self.bot.config['rules_messages']['7'])
        rules8 = await ch.fetch_message(self.bot.config['rules_messages']['8'])

        embed1=Embed(description=f"# Server Etiquette\n⦁ Try to maintain the natural flow of a conversation already in progress. Do not spam, post irrelevant images or purposely disrupt the chat in any way.\n⦁ Avoid sending repeating messages as well as repeated characters, emojis or phrases.\n⦁ Try to keep your messages together. Avoid breaking your paragraphs up into multiple lines and sending messages too quickly.\n⦁ Keep roleplay short and casual. The occasional head-pat, hug or high-five is fine, but limit non-conversation to only one or two messages.\n⦁ This is an English-speaking server. Please communicate in a way our members and staff can understand while participating in this server.", color=0x80F75C)

        embed2=Embed(description=f"# 2. Respect █\nExcessively argumentative, rude, dismissive, or aggressive members will be removed. We will not tolerate any instances of offensive behaviour towards anyone, nor any occurrences of racism, homophobia, transphobia or other types of discriminatory language. Jokes about these topics are equally unwelcome. Personal arguments or conversations between members should be taken to direct messages if both users wish to continue, rather than affecting the atmosphere/mood/feeling of the chat.", color=0x80F75C)

        embed3=Embed(description=f"# 3. Mental Illness\nThis includes jokes and discussing methods of harm. We care about the well-being of all our members; however, this chat is not a suitable method of mental care therapy. Instead, if you or somebody you know needs help, please seek out trained professionals for appropriate care. Resources relating to these issues can be found [Here](https://www.ispn-psych.org/mental-health-links).\n\n This rule isn't included in an attempt to deny people an emotional outlet, but instead to protect those members from malicious users who might try to convince them to harm themselves and to protect them from armchair psychologists who may make things worse.", color=0x80F75C)

        embed4=Embed(description=f"# 4. Staff Decisions\nIf any issue comes up, please ping the appropriate staff for assistance. Please do not attempt to resolve issues yourself. Staff's decisions and actions should be respected by all users; however users may contact the team for additional information, clarification or to appeal. If you have any issues with a particular staff's actions please take it to an <@&1104988250478743572> or <@&1109654196942282793> privately.\n\nIn the case of emergencies or issues that require immediate attention you can:\nPing us using <@&1068389119195107378> Please do not use this for non-emergencies.", color=0x80F75C)

        embed5=Embed(description=f"# 5. Advertising\nAdvertisements to other groups or Discord servers are not allowed without prior staff approval. Members seeking to advertise commissions or other products must do so in the art sectioned channels. Advertisements should not include any NSFW or otherwise unsuitable content. We consider raffles, or anything which requires following, liking, retweeting, and so forth, as advertising.\n\nChoosing to DM any member of the server only to try and advertise will result in an instant ban, especially if you are a low level member.", color=0x80F75C)

        embed6=Embed(description=f"# 6. Politics\nPolitical topics may be discussed, but must be held within the discussions channels (<#{self.bot.config['channels']['politics']}>⁠). Please try to avoid any heated political discussions. This includes, but is not limited to, inflammatory remarks, stances or controversial topics, takes or media. Political imagery or references are also not suitable for inclusion in profile pictures, nicknames or emojis. This ranges from Communist and Fascist symbolism, to modern day mainstream politics and political movements. Keep rule #2 in mind and treat each other with respect during discourse.", color=0x80F75C)

        embed7=Embed(description=f"# 7. NSFW Content\nNSFW Content is only allowed channels that are specifically marked as NSFW unless stated otherwise.\n⦁ All NSFW content should only be ART!\n⦁ Absolutely no real life NSFW images is allowed!\n⦁ Any extreme fetish, loli or anything against Discord TOS is NOT allowed!\n⦁ All NSFW content is subject to deletion and moderation by staff discretion.\nWe go to extreme links to make sure ONLY adults have access to NSFW areas, there is absolutely no exceptions to these rules for anyone!", color=0x80F75C)

        embed8=Embed(description=f"# 8. Alt Accounts\nDue to potential user abuse, users are not allowed to have alts within the server. If a user is found with an alt, the alt(s) and main account will be removed. Please keep any and all alts out of the server.", color=0x80F75C)

        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)
        await rules6.edit(content=f" ", embed=embed6)
        await rules7.edit(content=f" ", embed=embed7)
        await rules8.edit(content=f" ", embed=embed8)







    @Cog.listener('on_ready') #! ---> No Channels
    async def no_channels_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['info_channels']['no_channels']) #? No channels Channel

        msg1 = await ch.fetch_message(1133002927678697572) #? msg
        msg2 = await ch.fetch_message(1133009889204121701) #? msg
        msg3 = await ch.fetch_message(1133086049590059078) #? msg
        msg4 = await ch.fetch_message(1134113997378027582) #? msg
        msg5 = await ch.fetch_message(1134171819444805662) #? msg
        msg6 = await ch.fetch_message(1134568608979234846) #? msg
        
        
        
        lastmsg = await ch.fetch_message(1134568710112301086) #? msg

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(description=f"```fix\n█ Staff Hierarchy █\n```\n*These roles are in descending order.*\n\n***Executive Leading Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1104988250478743572>\n```\nObviously this role is for Owners of Serpent's Garden and in general make most of the decisions!\nNot usually an obtainable role.\n```\n<@&1109654196942282793>\n```\nThis role is for community managers.\nThey will manage the staff team / Game Server or Discord Server.\nObtainable after showing leadership as a council member.\n```\n<@&891793700932431942> \n```\nConsidered to be Head-Administrators as well as advisors for the Overseers & Overlord.\nObtainable after long term commitment as an administrator with no set time frame.\n```\n\n***Development Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1109655307682070558> \n```\nAchieved after continuously helping with development or providing services.\n```\n<@&1051307966223089755> \n```\nAchieved after providing development for servers on a regular basis.\n```\n\n***Moderation Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1020893519885373450> \n```\nThe highest form of moderation staff!\nObtainable after at least a year of commitment as a Senior Moderator.\n```\n<@&1055972422429442141> \n```\nOnce proven capable as a Junior Moderator you can be trusted as a regular moderator.\nObtained after at least a month after trial.\n```\n<@&1109665081681248266> \n```\nThis is the trial moderator role after being accepted to the staff team.\nObtained after application.\n```\n\n**Special Staff Roles**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1109656536978034718> \n```\nGiven on a per-case basis, for highly regarded members and retired staff.\n```", color=0x47F599)

        embed2=Embed(description=f"```fix\n█ Not able to see any channels? █\n```\nAre you not able to see any channels?  Or maybe you're missing some channels!?\n\n**You can get access to multiple different areas in the server using <id:customize>!**\n\nSerpent's Garden is a large community with many different areas that not everyone wants to be able to see!  That's why it is setup this way.", color=0x47F599)

        embed3=Embed(description=f"```fix\n█ Channel Quick Fix! █\n```\nIf you are looking for a quick fix becuase you've just recently lost access to some channels, or some have just disapeared.\n\n**Consider clicking `Show All Channels` as seen below!**", color=0x47F599)
        embed3.set_image(url="https://cdn.discordapp.com/attachments/550556052396179458/1133009744609673308/image.png")

        embed4=Embed(description=f"```fix\n█ The Access Roles! █\n```\n@everyone gets access to the public garden!\nChannels: General, gaming, memes.\n\n<@&1107421191586726039> gives access to channels related to the SCP:SL Servers.\nChannels: SL-Info, SL-Plugins, Round Reports\n\n<@&1129464175396143104> & <@&1158940507217608806> gives access to the server's primary channels!\nExamples: General, MayMays, media.\n\n<@&1116039697785950318> Razi's personal trans support group.\nChannels: Blahaj Chat, Blahaj Meetings.", color=0x47F599)

        embed5=Embed(description=f"```fix\n█ Serpent's Economy █\n```\nEvery new member joining the server is given **1,000x {coin} to start out with!**  You can gain these coins by sending messages in chat every couple of seconds.  Being in a vc for longer than 10 minutes, clicking on random rewards that appear and many other ways!  Usually when you gain coins you also are gaining XP as well!  The coins on the server have a finite amount to be more similar to an actual economy!\n\nThe Serpent bot itself gives its coins, when you or anyone else gains coins, along with that all the taxing and purchasing in the <#946730953731100682> goes to the Serpent!  Occasionaly coins are added in to the economy, to keep the Serpent bot from ever reaching 0 coins.\n\n**Taxation:** The bot usually will tax (ex: lottery winner) with an 8% tax!  This also applies to sending coins to another user on the server.  In addition to taxes on the movement & winnings of coins the bot taxes at a rate of **10x {coin} per hour**! This is just another measure to make sure inactive members with lots of coins, get their coins back in to the economy.", color=0x47F599)

        embed6=Embed(description=f"```fix\n█ Leaving Punishments █\n```\nAny member who decides to leave, is kicked or even banned.  Have all their coins given back to the Serpent!  So keep in mind if you ever decide to leave that you will not only lose all your coins!  But, any purchases you had made with those coins as well.\n\nThis is to keep the economy functioning properly and as another defensive measure against bad actors who get banned.", color=0x47F599)

        lastembed=Embed(description=f"```fix\n█ Table of Content █\n```\n\n1.) [Staff Hierarchy](https://discord.com/channels/689534383878701223/1133002668189700116/1133002927678697572)\n2.) [Not able to see any Channels?](https://discord.com/channels/689534383878701223/1133002668189700116/1133009889204121701)\n3.) [Channel Quick Fix](https://discord.com/channels/689534383878701223/1133002668189700116/1133086049590059078)\n4.) [The Access Roles](https://discord.com/channels/689534383878701223/1133002668189700116/1134113997378027582)\n5.) [Serpent's Economy](https://discord.com/channels/689534383878701223/1133002668189700116/1134171819444805662)\n6.) [Leaving Punishments](https://discord.com/channels/689534383878701223/1133002668189700116/1134568608979234846)", color=0x47F599)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)
        await msg6.edit(content=f" ", embed=embed6)

        await lastmsg.edit(content=f" ", embed=lastembed)









    @Cog.listener('on_ready')
    async def server_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['server_info']) #? role change Channel

        msg1 = await ch.fetch_message(1052828325422317578) #? msg
        msg2 = await ch.fetch_message(1052828331197874176) #? msg
        msg3 = await ch.fetch_message(1052828335283122196) #? msg

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(description=f"```fix\n█ Connecting to the Servers █\n```\nCurrently Serpent's Garden is only hosting our SCP Servers along side a spigot minecraft server!  Below you can find the IP addresses for joining these servers!\n\n**__Spigot Minecraft Server__**\n`mc.serpents.garden`\n\n\n**__SCP Server Addresses__**\n\n**[Alpha]**\n`connect n01.infra.serpents.garden:7777`", color=0xFF00FF)
        # embed1=Embed(description=f"```fix\n█ Connecting to the Servers █\n```\nCurrently Serpent's Garden is only hosting our SCP Servers along side a spigot minecraft server!  Below you can find the IP addresses for joining these servers!\n\n**__Spigot Minecraft Server__**\n`mc.serpents.garden`\n\n\n**__SCP Server Addresses__**\n\n**[Alpha]**\n`connect n01.infra.serpents.garden:7777`\n\n**[Gamma]**\n`connect n01.infra.serpents.garden:7778`\n\n**[Delta]**\n`connect n01.infra.serpents.garden:7779`\n\n**[Theta]**\n`connect n01.infra.serpents.garden:7780`\n\n**[Omega]**\n`connect n01.infra.serpents.garden:7781`\n\n", color=0xFF0000)


        embed2=Embed(description=f"```fix\n█ SCP:SL FAQ █\n```\n**Heres all of your usual questions answered!  You're welcome!**\n\n**What plugins does Serpent's Garden use?**\nWe use Universe, a private modding API and we created every plugin in house!  A list of all of our plugins can be found in <#1154301198619398194>!\n\n**What are all of these custom roles!?**\nYou always spawn as a custom role no matter the team!  A list of all of our custom roles can be found in <#1151144048015462461>!\n\n**What are all of the custom items added!?**\nJesus dude, are you blind? <#1151178974844702782>\n\n**How do I sync my roles from the Discord to the server?**\nThere is currently no way to do so...  Coming soon though... :3\n\n**Why is there LGBT Flags on surface!? >:o**\ngottem, L bozo!", color=0xFF0000)

        embed3=Embed(description=f"```fix\n█ Minecraft FAQ █\n```\n**All your Minin' and Craftin' questions all answered!**\n\n**What plugins does Serpne's Garden use?**\nI'll never tell!\n\n**Why can't I play without having the resource pack?**\nYou will literally die to invisible creepers if you don't...\n\n**Why is the server SO gooooood!**\nBecause it is. Period.", color=0x00FFFF)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)








def setup(bot):
    x = rules_handler(bot)
    bot.add_cog(x)