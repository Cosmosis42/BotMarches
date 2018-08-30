#Frequently Asked Questions

from discord.ext import commands
from pickle import loads, dumps

whitelist = [
    '106449616681062400', #Admin1
    '107085990652280832', #Admin2
    '209840589166870528' #me
]
class FaqModule:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.questions = loads(self.bot.redis.get('questions'))
        except:
            self.questions = list()

    @commands.command()
    async def faq(self, ctx): #Arbitrary number of arguments
            wrapper = '```'
            output = '{}\n'.format(wrapper)
            for index in range(0, len(self.questions)):
                form_args = (index + 1, self.questions[index])
                output += '{})\t{}\n'.format(*form_args)
            
            output += wrapper
            await ctx.send(output)
    
    @commands.command(hidden=True)
    async def faq_add(self, ctx, question):
            self.questions.append(question)
            self.bot.redis.set('questions', dumps(self.questions))
            await ctx.send('Question added.')


def setup(bot):
    bot.add_cog(FaqModule(bot))