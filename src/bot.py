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

vowels = 'aeiouy'

animals_req = urlopen('https://gist.githubusercontent.com/atduskgreg/3cf8ef48cb0d29cf151bedad81553a54/raw/82f142562cf50b0f6fb8010f890b2f934093553e/animals.txt')
animals = animals_req.read().decode().split('\n')
animals = [x for x in animals if len(x) > 0]

adjective_req = urlopen('https://raw.githubusercontent.com/aaronbassett/Pass-phrase/master/adjectives.txt')
adjectives = adjective_req.read().decode(errors='replace').split('\n')
adjectives = [x for x in adjectives if len(x) > 0]

verb_req = urlopen('https://raw.githubusercontent.com/aaronbassett/Pass-phrase/master/verbs.txt')
verbs = verb_req.read().decode().split('\n')
verbs = [x for x in verbs if len(x) > 0]
for idx in range(0, len(verbs)):
        if verbs[idx][-1] in vowels:
            verbs[idx] = verbs[idx][0:-1] + 'ing'
        else:
            verbs[idx] += 'ing'

objects_req = urlopen('https://raw.githubusercontent.com/aaronbassett/Pass-phrase/master/nouns.txt')
objects = objects_req.read().decode().split('\n')
objects = [x for x in objects if len(x)>0]



initial_extensions = [
    'cogs.misc',
    'cogs.dice',
    'cogs.faq', 
    'cogs.event',
    'cogs.rumour'
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
        self.verbs = verbs
        self.objects = objects

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