try:
    import discord
except:
    from subprocess import check_output
    check_output(['pip', 'install', '-U', 'https://github.com/Rapptz/discord.py/archive/rewrite.zip'])
    import discord
    
from discord.ext import commands
from os import environ
import logging
import redis
from urllib.request import urlopen

logging.basicConfig(level=logging.INFO)

AUTH_TOKEN = environ['DISCORD_TOKEN']
REDIS_URL = environ['REDISTOGO_URL']

animals_req = urlopen('https://gist.githubusercontent.com/atduskgreg/3cf8ef48cb0d29cf151bedad81553a54/raw/82f142562cf50b0f6fb8010f890b2f934093553e/animals.txt')
animals = animals_req.read().decode().split('\n')
adjective_req = urlopen('https://www.d.umn.edu/~rave0029/research/adjectives1.txt')
adjectives = adjective_req.read().decode(errors='replace').split('\n')

initial_extensions = [
    'cogs.misc',
    'cogs.dice',
    'cogs.faq', 
    'cogs.event'
]
class WestMarchesBot(commands.Bot):
    def __init__(self):
        super().__init__(commands.when_mentioned_or('&'), 
                        description='I will help you organize your game.', #Description shows up in help dialog
                        pm_help=True,
                        command_not_found="I dunno what yer talkin' about, {}.")
        
        self.redis = redis.from_url(REDIS_URL)
        self.animals = animals
        self.adjectives = adjectives

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