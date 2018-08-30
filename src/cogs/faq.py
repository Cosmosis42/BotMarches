#Frequently Asked Questions

from discord.ext import commands
from pickle import loads, dumps

class FaqModule:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.questions = loads(self.bot.redis.get('questions'))
        except:
            self.questions = list()

    @commands.command(hidden=True)
    async def faq(self, ctx, *arguments): #Arbitrary number of arguments
        await ctx.send(arguments)


def setup(bot):
    bot.add_cog(FaqModule(bot))