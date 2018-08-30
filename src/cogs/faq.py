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

    @commands.command(hidden=True)
    async def faq(self, ctx, *arguments): #Arbitrary number of arguments
        '''Frequently asked questions.'''
        if arguments[0] is not 'add':
            wrapper = '```'
            output = '{}\n'.format(wrapper)
            for index in range(0, len(self.questions)):
                form_args = (index + 1, self.questions[index])
                output += '{})\t{}\n'.format(*form_args)
            
            output += wrapper
            await ctx.send(output)
        elif ctx.author in whitelist:
            input_question = str()
            for item in arguments[1:]:
                input_question += '{} '.format(item)

            self.questions.append(input_question)
            self.bot.redis.set('questions', dumps(self.questions))
            await ctx.send('Question added.')


def setup(bot):
    bot.add_cog(FaqModule(bot))