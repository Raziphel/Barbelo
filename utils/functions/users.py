# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel

from asyncio import sleep
from random import randint, choice
from math import floor

import utils

class UserFunctions(object):
    bot = None





    @classmethod
    async def revive_user(cls, user:Member):
        '''Brings a user back to life, or to life for the first time!'''

        guild = cls.bot.get_guild(cls.bot.config['guild_id'])
        alive = utils.DiscordGet(guild.roles, id=cls.bot.config['alive'])
        dead = utils.DiscordGet(guild.roles, id=cls.bot.config['dead'])

        #+ Send joining server messages!
        if alive not in user.roles:
            if dead not in user.roles:
                log = cls.bot.get_channel(cls.bot.config['channels']['general'])
                await log.send(content=f"<@&{cls.bot.config['ping_roles']['welcomer']}> {user.mention}", embed=utils.Embed(color=randint(1, 0xffffff), title=f"{user.name} has joined Esoterica."))

                #? Assign new member roles.
                entry_role_ids = [cls.bot.config['seperator_roles']['access'], 
                                    cls.bot.config['seperator_roles']['purchases'], 
                                    cls.bot.config['seperator_roles']['pings'], 
                                    cls.bot.config['seperator_roles']['about'],
                                    cls.bot.config['access_roles']['alive']],

                for role_id in entry_role_ids:
                    role = utils.DiscordGet(guild.roles, id=role_id)
                    await user.add_roles(role, reason="Joined Server!")

        #! Add a way to revive dead people later.

        #* Makes sure they get have the correct level role.
        await cls.check_level(user)





    @classmethod
    async def level_up(cls, user:Member, channel:TextChannel=None):
        '''Checks if they should level up and then levels then up!'''

        #? Set Varibles
        lvl = utils.Levels.get(user.id)
        c = utils.Coins.get(user.id)

        #? Check if they should even level up!
        requiredexp = await cls.determine_required_exp(lvl.level)
        if lvl.exp < requiredexp:
            return

        #+ Level em the hell up!
        lvl.exp = 0
        lvl.level += 1
        coins = (lvl.level*2500)

        await utils.CoinFunctions.earn(earner=user, amount=coins)

        async with cls.bot.database() as db:
            await lvl.save(db)
            await c.save(db)

        #? Check for a role change.
        await cls.check_level(user=user)

        #? Log it and tell em.
        if channel:
            msg = await channel.send(embed=utils.Embed(color = randint(1, 0xffffff), desc=f"🎉 {user.mention} is now level: **{lvl.level:,}**\nGranting them: **{coins:,}**"))

        log = cls.bot.get_channel(cls.bot.config['logs']['coins'])
        await log.send(f"**<@{user.id}>** leveled up and is now level **{lvl.level:,}**\nGranting them: **{coins:,}**")

        await sleep(6)
        try: await msg.delete()
        except: pass



    @classmethod
    async def determine_required_exp(cls, level:int):
        """Determines how much exp is needed to level up!"""
        if level == 0:
            requiredexp = 10
        elif level < 4:
            requiredexp = level*25
        else:
            requiredexp = round(level**2.75)
        return requiredexp


    @classmethod
    async def check_level(cls, user:Member):
        """Checks the highest level role that the given user is able to receive"""

        # Get the users
        guild = cls.bot.get_guild(cls.bot.config['guild_id'])
        lvl = utils.Levels.get(user.id)

        level_roles = {
            90: "lvl.90",
            80: "lvl.80",
            70: "lvl.70",
            60: "lvl.60",
            50: "lvl.50",
            40: "lvl.40",
            30: "lvl.30",
            20: "lvl.20",
            10: "lvl.10",
            0: "lvl.0"
        }

        # Get roles from the user we'd need to delete
        try:
            role_to_delete = [i for i in user.roles if i.name in level_roles.values()]
        except IndexError:
            role_to_delete = None

        # Get role that the user is viable to have
        viable_level_roles = {i:o for i, o in level_roles.items() if lvl.level >= i}
        if viable_level_roles:
            role_to_add = viable_level_roles[max(viable_level_roles.keys())]
        else:
            role_to_add = None

        # Add the roles
        if role_to_delete:
            await user.remove_roles(*role_to_delete, reason="Removing Level Role.")

        if role_to_add:
            try:
                role = utils.DiscordGet(guild.roles, name=role_to_add)
                await user.add_roles(role, reason="Adding Level Role.")
            except: 
                print(f'Failed to apply level role: {user.name} getting role: {role_to_add}')