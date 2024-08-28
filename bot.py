import os
from glob import glob

from discord import Intents

from barbelo import Barbelo


intents = Intents.all()
bot = Barbelo(
    command_prefix=["."],
    config="config/config.toml",
    secret="config/secret.toml",
    intents=intents
)
logger = bot.logger
extensions = [i.replace(os.sep, '.')[:-3] for i in glob("cogs/*/[!_]*.py")]


if __name__ == "__main__":
    """Starts the bot, loading all of the extensions"""

    logger.info(f"Loading {len(extensions)} extensions")
    print(f"Loading {len(extensions)} extensions")
    for extension in extensions:
        try:
            print(f"Loaded: {extension}")
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load {extension}")
            raise e
    bot.run()
