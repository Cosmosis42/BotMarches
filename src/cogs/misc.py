#Misc commands

from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

GUILDHALL = 483022288870965259

class MiscModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Marco?
        Polo!"""
        await ctx.send('pong')

    @commands.command()
    async def echo(self, ctx, *, message):
        """ECHO Echo echo
        echo..."""
        await ctx.send(message)

    @commands.command(hidden=True)
    async def gh(self, ctx, *, message):
        channel = self.bot.get_channel(GUILDHALL)
        logging.info('GH: {}'.format(message))
        msg = await channel.send(message)
        logging.info('Response: {}'.format(str(msg)))


def setup(bot):
    bot.add_cog(MiscModule(bot))