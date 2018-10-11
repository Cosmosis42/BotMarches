#Misc commands

from discord.ext import commands

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
    async def gh(self, ctx, * ,message):
        channel = self.bot.get_channel(GUILDHALL)
        await channel.send(message)


def setup(bot):
    bot.add_cog(MiscModule(bot))