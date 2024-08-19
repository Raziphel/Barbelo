import colorsys
import typing
from collections import Counter
from io import BytesIO
from math import floor

import discord
from PIL import Image, ImageDraw, ImageFont
from discord import Member, ApplicationCommandOption, ApplicationCommandOptionType, File, NotFound
from discord.ext.commands import command, Cog, BucketType, cooldown, ApplicationCommandMeta

import utils

Number = int | float

# base_image_size = (475, 356)
base_image_size = (375, 281)

resources_directory = "resources"

level_details_x = 100
parent_progress_bar_h_w = (113, 25)
parent_progress_bar_x_y = (17, 161)
inner_progress_bar_padding = 2.5  # px
progress_bar_color = "aqua"

# Font settings #

ttf_font_path = f'{resources_directory}/SourceSansPro-Regular.ttf'
ttf_bold_font_path = f'{resources_directory}/SourceSansPro-SemiBold.ttf'
ttf_italic_font_path = f'{resources_directory}/SourceSansPro-Italic.ttf'

# The default size for all text that's not the username, title (i.e. their highest Discord role), or the progress bar.
default_ttf_size = 19

username_ttf_size = 24
title_ttf_size = 20
progress_bar_ttf_size = 13

fnt = ImageFont.truetype(ttf_font_path, default_ttf_size)
username_fnt = ImageFont.truetype(ttf_bold_font_path, username_ttf_size)
title_fnt = ImageFont.truetype(ttf_italic_font_path, title_ttf_size)
progress_bar_fnt = ImageFont.truetype(ttf_font_path, progress_bar_ttf_size)


def determine_primary_color(image):
    # Load the image and convert it to the RGB color space
    image = image.convert('RGB')

    # Resize the image to a smaller size
    image = image.resize((50, 50))

    # Get the pixel data of the image
    pixels = image.getdata()

    # Count the number of occurrences of each color using a Counter object
    color_count = Counter(pixels)

    # Find the color with the highest count
    primary_color = color_count.most_common(1)[0][0]

    return primary_color


def calculate_contrasting_color(background_color):
    # Convert the background color to the HSV color space
    h, s, v = colorsys.rgb_to_hsv(*background_color)

    # Calculate the value of the background color
    value = max(background_color) / 255

    # Choose a text color based on the value of the background color
    if value < 0.5:
        text_color = (255, 255, 255)  # white
    else:
        text_color = (0, 0, 0)  # black

    return text_color


def calculate_xy_size(
        x: Number,
        y: Number,
        height: Number,
        width: Number
) -> typing.Tuple[Number, Number, Number, Number]:
    """A helper function for simply calculating an image's size."""
    return (
        x,
        y,
        x + height,
        y + width
    )


def format_number(num):
    if num < 1000:
        return str(floor(num))
    elif num < 1000000:
        return f"{num / 1000:.1f}k"
    elif num < 1000000000:
        return f"{num / 1000000:.1f}m"
    else:
        return f"{num / 1000000000:.1f}b"


class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        aliases=['p', 'P', 'Profile'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user you want to get the profile of.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        ),
    )
    async def profile(self, ctx, user: Member = None):
        '''Shows a user's profile'''
        if not user:
            user = ctx.author

        # await self.base_profile(ctx=ctx, user=user, msg=None)
        file = await self.generate_screenshot(user)

        # await ctx.send(file=file)
        await ctx.interaction.response.send_message(file=file)

    async def get_user_avatar(self, member: Member) -> BytesIO:
        avatar = member.display_avatar

        try:
            data = await avatar.read()

        except NotFound:
            # Avatar was changed and our cache wasn't updated for whatever reason
            user = await self.bot.fetch_user(member.id)
            avatar = user.display_avatar
            data = await avatar.read()

        return BytesIO(data)

    def get_level_rank(self, member: discord.Member) -> int:
        sorted_levels = utils.Levels.sort_levels()
        member_level = utils.Levels.get(member.id)
        try:
            level_rank = sorted_levels.index(member_level)

            return level_rank + 1  # Add 1 because indexes start from 0
        except ValueError:  # User is not in the list yet maybe?
            return -1

    def get_wealth_rank(self, member: discord.Member) -> int:
        sorted_wealth = utils.Currency.sort_coins()
        member_wealth = utils.Currency.get(member.id)
        try:
            wealth_rank = sorted_wealth.index(member_wealth)

            return wealth_rank + 1
        except ValueError:
            return -1

    async def generate_screenshot(self, member: Member):
        moderation = utils.Moderation.get(member.id)
        levels = utils.Levels.get(member.id)
        currency = utils.Currency.get(member.id)
        tracking = utils.Tracking.get(member.id)

        if levels.level == 0:
            required_exp = 10
        elif levels.level < 5:
            required_exp = levels.level * 25
        else:
            required_exp = round(levels.level ** 2.75)

        avatar = await self.get_user_avatar(member)
        username = str(member.name)
        title = str(member.top_role)
        current_level = levels.level
        current_experience = floor(levels.exp)
        badges = []  # TODO: replace with real data
        networth = format_number(currency.coins)
        messages = format_number(tracking.messages)

        voice_activity = floor(tracking.vc_mins / 60)
        voice_activity = format_number(voice_activity)

        level_rank = self.get_level_rank(member)
        wealth_rank = self.get_wealth_rank(member)

        experience_percentage = current_experience / required_exp
        relative_inner_progress_bar_width = experience_percentage * parent_progress_bar_h_w[0]

        # Create a new page and set the HTML content of the page
        progress_bar = Image.new(
            mode='RGBA',
            size=parent_progress_bar_h_w,
            color="white"
        )

        # Prepare to draw text as well as the inner and outer progress bars
        progress_bar_draw = ImageDraw.Draw(progress_bar)

        # Draw progress bar outline
        progress_bar_draw.rectangle(
            (
                0, 0,
                parent_progress_bar_h_w[0] - 0.1,
                parent_progress_bar_h_w[1] - 0.1
            ),
            fill="white",
            outline="black"
        )

        # Draw inner progress bar
        inner_progress_bar_size = calculate_xy_size(
            inner_progress_bar_padding,
            inner_progress_bar_padding,
            relative_inner_progress_bar_width,  # User's progress towards their next level
            parent_progress_bar_h_w[1] - inner_progress_bar_padding * 2
        )

        progress_bar_draw.rectangle(
            inner_progress_bar_size,
            fill=progress_bar_color
        )

        # Center alignment for progress bar text
        progress_bar_text_x_y = (
            progress_bar.size[0] / 2,
            progress_bar.size[1] / 2
        )

        # Add the text to the progress bar
        progress_bar_draw.text(
            progress_bar_text_x_y,
            f'XP: {current_experience:,} / {required_exp:,}',
            font=progress_bar_fnt,
            fill="black",
            anchor="mm",
            align="center"
        )

        progress_bar.putalpha(225)

        # Create our base image
        canvas = Image.new('RGBA', base_image_size, color=128)

        # User's background image
        background = Image.open(f'{resources_directory}/default-background.jpg')
        canvas.paste(background)

        # Determine the primary color of the background
        primary_color = determine_primary_color(background)

        # Calculate a contrasting color for the primary color
        text_color = calculate_contrasting_color(primary_color)

        draw = ImageDraw.Draw(canvas)

        # Draw the main border
        draw.rectangle(
            xy=calculate_xy_size(
                4, 4,
                canvas.size[0] - 8,
                canvas.size[1] - 8
            ),
            outline=text_color,
            width=3
        )

        # Place the user's profile picture on the canvas
        profile_picture = Image.open(avatar).convert('RGBA')

        # Determine the primary color of the background
        profile_picture_primary_color = determine_primary_color(profile_picture)

        # Draw the border we'll be putting the avatar in using the avatar's primary color
        draw.rectangle(
            xy=calculate_xy_size(18, 18, 110, 110),
            outline=profile_picture_primary_color,
            width=1
        )

        # noinspection PyUnresolvedReferences
        profile_picture = profile_picture.resize((103, 103), Image.Resampling.LANCZOS)
        canvas.paste(profile_picture, (22, 22))

        draw.text(
            xy=(38 if current_level > 10 else 40, 132),
            text=f'Level {current_level}',
            fill=text_color,
            font=fnt
        )

        # Temporary solution for long usernames? In the future, it'd be nice to adjust the text's size dynamically so
        # that it fits. Although we will have to set a limit either way, so..
        if len(username) > 16:
            username = username[:16] + '..'

        draw.text(
            xy=(140, 20),
            text=username,
            fill=text_color,
            font=username_fnt
        )

        draw.text(
            xy=(140, 50),
            text=title,
            fill=text_color,
            font=title_fnt
        )

        draw.text(
            xy=(17, 190),
            text=f'Level rank:  {level_rank}#',  # Extra spacing to line up the ranks
            fill=text_color,
            font=fnt
        )

        draw.text(
            xy=(17, 215),
            text=f'Coin rank:   {wealth_rank}#',
            fill=text_color,
            font=fnt
        )

        # Toss in all the basic information
        speech_balloon = Image.open(f'{resources_directory}/speech-balloon.png').convert('RGBA').resize((27, 27))
        canvas.alpha_composite(speech_balloon, dest=(140, 90))

        draw.text(
            xy=(168, 90),
            text=f': {messages} Messages',
            fill=text_color,
            font=fnt
        )

        microphone = Image.open(f'{resources_directory}/microphone-3.png').convert('RGBA').resize((27, 27))
        canvas.alpha_composite(microphone, dest=(140, 123))

        draw.text(
            xy=(168, 123),
            text=f': {voice_activity} VC hours',
            fill=text_color,
            font=fnt
        )

        coin = Image.open(f'{resources_directory}/gold-coin.png').convert('RGBA').resize((27, 27))
        canvas.alpha_composite(coin, dest=(140, 156))

        draw.text(
            xy=(168, 156),
            text=f': {networth} Coins',
            fill=text_color,
            font=fnt
        )

        # Add progress bar to the base image
        canvas.alpha_composite(progress_bar, dest=parent_progress_bar_x_y)

        # Badges
        """
        This is for testing purposes only.
        blue_diamond = Image.open('large-blue-diamond.png').convert('RGBA').resize((33, 33))
        canvas.alpha_composite(blue_diamond, dest=(30, 200))

        cross_mark = Image.open('cross-mark.png').convert('RGBA').resize((33, 33))
        canvas.alpha_composite(cross_mark, dest=(80, 200))
        """

        buffer = BytesIO()
        canvas.save(buffer, "png")
        buffer.seek(0)
        canvas.close()

        file = File(buffer, filename='profile.png')

        return file


    # async def base_profile(self, ctx, user, msg):
    #     if msg == None:
    #         msg = await ctx.send(embed=utils.ProfileEmbed(type="Default", user=user))
    #     else:
    #         await msg.edit(embed=utils.ProfileEmbed(type="Default", user=user))

    #     await msg.clear_reactions()
    #     # ! adds the reactions
    #     if ctx.channel.id in self.bot.config['fur-channels'].values():
    #         await msg.add_reaction("✨")
    #     if ctx.channel.id in self.bot.config['nsfw-fur-channels'].values():
    #         await msg.add_reaction("🔞")
    #     # for role in user.roles:
    #     #     if role.id == self.bot.config['roles']['council']:
    #     #         await msg.add_reaction("🍃")

    #     # Watches for the reactions
    #     check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["✨", "🍃"]
    #     r, _ = await self.bot.wait_for('reaction_add', check=check)
    #     if ctx.channel.id in self.bot.config['fur-channels'].values():
    #         if r.emoji == "✨":
    #             await msg.edit(embed=utils.ProfileEmbed(type="Sfw_Sona", user=user))
    #             pass
    #     if r.emoji == "🍃":
    #         await msg.edit(embed=utils.ProfileEmbed(type="Staff-Track", user=user))
    #         pass
    #     await msg.clear_reactions()
    #     await msg.add_reaction("🔷")
    #     check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["🔷"]
    #     r, _ = await self.bot.wait_for('reaction_add', check=check)
    #     if r.emoji == "🔷":
    #         await self.base_profile(ctx=ctx, user=user, msg=msg)
    #         return




    @command(application_command_meta=ApplicationCommandMeta(), aliases=['i', 'inv', 'items', 'Inv'])
    async def inventory(self, ctx, user:Member=None):
        '''Quick Check inventory'''
        if not user:
            user = ctx.author
        await ctx.interaction.response.send_message(embed=utils.Embed(type="Items", user=user, quick=True))



    @cooldown(1, 5, BucketType.user)
    @command(aliases=['color', 'Color', 'Setcolor', 'SetColor'],
            application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="colour",
                    description="the color you are wanting...",
                    type=ApplicationCommandOptionType.string,
                    required=False
                    )
                ],
            ),
        )
    async def setcolor(self, ctx, colour=None):
        '''Sets your user color'''

        if colour == None:
            file = discord.File('config/lists/colors.py', filename='config/lists/colors.py')
            await ctx.interaction.response.send_message(f"**Heres a list of colors you can use!**", file=file)
            return

        colour_value = utils.Colors.get(colour.lower())
        tr = utils.Tracking.get(ctx.author.id)

        if colour_value == None:
            try:
                colour_value = int(colour.strip('#'), 16)
            except ValueError:
                await ctx.interaction.response.send_message(embed=utils.Embed(title="Incorrect colour usage!"))
                return

        tr.color = colour_value
        async with self.bot.database() as db:
            await tr.save(db)

        await ctx.interaction.response.send_message(embed=utils.Embed(title="Your color setting has been set!", user=ctx.author))

def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
