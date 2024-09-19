
from discord import Embed, RawReactionActionEvent
from discord.ext.commands import Cog 

import utils


class server_info(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #+ The Server Logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['logs']['server']) 


    @Cog.listener()
    async def on_ready(self):
        """Displays the role handler messages"""
        ch = self.bot.get_channel(self.bot.config['channels']['server_info'])

        msg1 = await ch.fetch_message(self.bot.config['server_info_messages']['1'])
        msg2 = await ch.fetch_message(self.bot.config['server_info_messages']['2'])
        msg3 = await ch.fetch_message(self.bot.config['server_info_messages']['3'])

        embed1=Embed(description=f"# Age\n```\nLying about your age will result in a ban!\n```\n> 🚬<@&{self.bot.config['age_roles']['adult']}>`Gives access to adult only channels!`\n> 🍼<@&{self.bot.config['age_roles']['underage']}>`Given automatically if you don't get an age role.`", color=0x8f00f8)

        embed2=Embed(description=f"# Pings\n```\nGet notifications for things!\n```\n> 📔<@&{self.bot.config['ping_roles']['changelogs']}> `Recommended! Get pinged about changes!`\n> ✅<@&{self.bot.config['ping_roles']['voters']}> `Get pinged when a vote is held!`\n> 📆<@&{self.bot.config['ping_roles']['events']}> `Get pinged for info on server events!`\n> 🤝<@&{self.bot.config['ping_roles']['welcomer']}> `Get pinged to greet any new members!`\n> 📊<@&{self.bot.config['ping_roles']['server_status']}> `Get pinged when our servers are down!`", color=0x8f00f8)

        embed3=Embed(description=f"# Access\n```\nWhat parts of the server would you like to see!\n```\n> 🚧<@&{self.bot.config['access_roles']['scpsl']}>`Gives access to the SCP:SL section.`\n> 🎀<@&{self.bot.config['access_roles']['queer']}>`Gives access to the Degen Girls section.`\n> 🚬<@&{self.bot.config['access_roles']['shitposters']}>`Gives access to the Toxic Boys section.`", color=0x8f00f8)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)



def setup(bot):
    x = server_info(bot)
    bot.add_cog(x)