try:
    import discord
except:
    from subprocess import check_output
    check_output(['pip', 'install', '-U', 'https://github.com/Rapptz/discord.py/archive/rewrite.zip'])
    import discord
    
from discord.ext import commands
from os import environ
import logging

logging.basicConfig(level=logging.INFO)

AUTH_TOKEN = environ['DISCORD_TOKEN']
#REDIS_URL = environ['REDISTOGO_URL']

initial_extensions = [
    'cogs.misc',
    'cogs.dice'
]
class WestMarchesBot(commands.Bot):
    def __init__(self):
        super().__init__(commands.when_mentioned_or('&'), 
                        description='I will help you organize your game.', #Description shows up in help dialog
                        pm_help=True,
                        command_not_found="I dunno what yer talkin' about, {}.")

    async def on_ready(self):
        logging.info('Logged in.')
        logging.info('Are you ready now, Mr. Krabs?')

        game = '&help'
        #Display help command as 'game being played'
        await super().change_presence(activity=discord.Game(name=game, type=1))

if __name__ == '__main__':
    scribe = WestMarchesBot()

    logging.info('Loading extensions')
    for extension in initial_extensions:
        scribe.load_extension(extension)
    
    logging.info('Starting.')
    scribe.run(AUTH_TOKEN)
    logging.info('Exited.')