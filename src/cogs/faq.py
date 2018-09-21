#Frequently Asked Questions

from discord import Embed, Colour
from discord.ext import commands
from pickle import loads, dumps
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)

FaqEmbed = Embed(
            title='Frequently Asked Questions (CLICK ME)',
            url='http://evantyr.wiki/Guidelines',
            type='rich',
            author='Corbin',
            colour=Colour.from_rgb(23, 160, 101)
        )

pageUrl = 'http://evantyr.wiki/Guidelines'
page = urlopen(pageUrl).read()

soup = BeautifulSoup(page, 'html.parser')

unordered_lists = soup.findAll('ul')

for ui in unordered_lists:
    if "How many characters am I allowed to have?" in str(ui):
        faq = ui.findAll('li')
        break

parsedFaq = list()
for entry in faq:
    question = str(entry.find('b'))
    question = question.strip('</b>')
    answer = str(entry.find('dd'))
    answer = answer.strip('</d>')
    parsedFaq.append((question, answer))

for pair in parsedFaq:
    FaqEmbed.add_field(name=pair[0], value=pair[1], inline=False)

class FaqModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faq(self, ctx):
        await ctx.send(embed=FaqEmbed)


def setup(bot):
    bot.add_cog(FaqModule(bot))