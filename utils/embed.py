# Discord
from discord import Embed
from discord.ext.commands import command, Cog
from random import choice

import utils

class DefaultEmbed(Embed):
    bot = None

    def __init__(self, *args, **kwargs):
        #?Gets the varibles for the embed
        user = kwargs.pop('user', None)
        title = kwargs.pop('author', None)
        thumbnail = kwargs.pop('thumbnail', None)
        image = kwargs.pop('image', None)
        desc = kwargs.pop('desc', None)
        guild = kwargs.pop('guild', None)
        footer = kwargs.pop('footer', None)

        #+ Make the Embed
        super().__init__(*args, **kwargs)

        #* Add Color
        if user:
            t = utils.Tracking.get(user.id)
            self.color = t.color

        #* Add Author
        if title:
            self.set_author(name=title, url=patron)

        #* Add Thumbnail
        if thumbnail:
            self.set_thumbnail(url=thumbnail)

        #* Add Image
        if image:
            self.set_image(url=image)

        #* Add Description
        if desc:
            self.description = f"{desc}"

        #* Add Footer
        if footer:
            self.set_footer(text=footer)