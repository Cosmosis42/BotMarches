try:
    import discord
except:
    from subprocess import check_output
    check_output(['pip', 'install', '-U', 'https://github.com/Rapptz/discord.py/archive/rewrite.zip'])
    import discord
    
from discord.ext import commands
from os import environ

AUTH_TOKEN = environ['DISCORD_TOKEN']
#REDIS_URL = environ['REDISTOGO_URL']

client = commands.Bot(command_prefix = '&')

@client.event
async def on_ready():
    print('Are you ready now, Mr. Krabs?')

client.run(AUTH_TOKEN)