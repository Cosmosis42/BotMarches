#Dice commands

from discord.ext import commands
import re #Regular Expressions
import random #Random number gen


class DiceModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *, message):
        """Roll the dice! 1d20+4"""
        matches = re.findall(r'(\d*)d(\d+)(\s*[+-]\s*\d+)?', message)
        total = int()
        for a, b, c in matches: #a dice, b sides, c modifier
            c = c.replace(' ', '') #Remove white space incase someone has ' + 4' or such
            for dice in range(0, int(a)):
                total += random.randint(1, int(b))
            total += int(c or 0)

        output = 'You rolled {}'.format(total)
        await ctx.send(output)                    


def setup(bot):
    bot.add_cog(DiceModule(bot))