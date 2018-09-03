#Frequently Asked Questions

from discord import Embed, Colour
from discord.ext import commands
from pickle import loads, dumps
import logging

logging.basicConfig(level=logging.INFO)

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
            self.answers = loads(self.bot.redis.get('answers'))
        except:
            self.questions = list()
            self.answers = list()

    @commands.command(hidden=True)
    async def faq_old(self, ctx): #Arbitrary number of arguments
        '''Frequently assked questions.'''
        wrapper = '```'
        output = '{}Frequently asked questions:\n'.format(wrapper)

        for index in range(0, len(self.questions)):
            form_args = (index + 1, self.questions[index])
            output += '{})\t{}\n'.format(*form_args)
            
        output += wrapper
        await ctx.send(output)
    
    @commands.command(hidden=True)
    async def faq_add(self, ctx, question):
        if ctx.author in whitelist:
            self.questions.append(question)
            self.bot.redis.set('questions', dumps(self.questions))
            await ctx.send('Question added.')
        else:
            logging.info('{} requested an addition but is not whitelisted.'.format(ctx.author))

    @commands.command()
    async def faq(self, ctx):
        FaqEmbed = Embed(
            title='Frequently Asked Questions',
            type='rich',
            author='Corbin',
            colour=Colour.from_rgb(23, 160, 101)
        )
        for idx in range(0, len(self.questions)):
            question = self.questions[idx]
            
            if idx < len(self.answers):
                answer = self.answers[idx]
            else:
                answer = 'Null answer.'

            FaqEmbed.add_field(name=question, value=answer, inline=False)

        await ctx.send(embed=FaqEmbed)


def setup(bot):
    bot.add_cog(FaqModule(bot))