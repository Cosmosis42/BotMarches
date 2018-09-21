#Frequently Asked Questions

from discord import Embed, Colour
from discord.ext import commands
from pickle import loads, dumps
import logging

logging.basicConfig(level=logging.INFO)

FaqEmbed = Embed(
            title='Frequently Asked Questions (CLICK ME)',
            url='http://evantyr.wiki/Guidelines',
            type='rich',
            author='Corbin',
            colour=Colour.from_rgb(23, 160, 101)
        )

faq = [
    (
        'How many characters am I allowed to have?',
        'There is no limit to how many characters you can have. Just remember, the XP you earn is specific to your character!'
    ),
    (
        'The character option I want was published in two books, which should I use?',
        'The most recent publication of any given character option should be used.'
    ),
    (
        'Can I trade items to other characters?',
        'Yes. However, you can not trade items between two of your own characters. Any items traded, must end up in the possession of a different player.'
    ),
    (
        "I'm playing a Cleric and/or some other religious character. What god(s) am I allowed to worship?",
        "You can worship any god you like! We don't use any specific pantheon here. Just be sure to check Category:Deities first, and see if the god you wish to worship is listed there. If not, you can make a new page for it! Once a page for your god exists on the wiki, that god now exists within the lore of Evantyr!"
    ),
    (
        "One of my characters has gone on a multi-session adventure. We haven't finished yet, but there is another adventure I'd like to play in. What do?",
        "You can still play in other adventures while one of your characters is away on a multi-session adventure. However, your character can't be in two places at once. In order to play in the second adventure, you must play as a different character."
    )
]

for pair in faq:
    FaqEmbed.add_field(name=pair[0], value=pair[1], inline=False)

class FaqModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faq(self, ctx):
        await ctx.send(embed=FaqEmbed)


def setup(bot):
    bot.add_cog(FaqModule(bot))