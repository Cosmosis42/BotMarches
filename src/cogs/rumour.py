from discord import Embed, Colour
from discord.ext import commands
from pickle import loads, dumps
from random import randint

RUMOURS = 483023103555928085

class rumour:
    def __init__(self, id, description, gm, poster, msgID=None):
        self.description = description
        self.gm = gm
        self.eventID = id
        self.msgID = msgID
        self.poster = poster

    def embed(self):
        temp = Embed(
            title='ID: {}'.format(self.eventID),
            type='rich',
            author='Corbin',
            colour=Colour.from_rgb(23, 160, 101)
        )

        temp.add_field(name='**Description:**', value=self.description)
        temp.add_field(name='**GM**', value=self.gm, inline=False)
        temp.add_field(name='Posted by:', value='@{'+self.poster.id+'}', inline=False)
        return(temp)

class RumoursModule:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.rumours = loads(self.bot.redis.get('rumours'))
        except:
            self.rumours = list()

        try:
            self.usedKeys = loads(self.bot.redis.get('usedKeys'))
        except:
            self.usedKeys = list()

    def IDgen(self):
        while True:
            self.usedKeys = loads(self.bot.redis.get('usedKeys'))
            verb = randint(0, len(self.bot.verbs))
            obj_idx = randint(0, len(self.bot.objects))
            key_tup = (verb, obj_idx)
            if key_tup not in self.usedKeys:
                self.usedKeys.append(key_tup)
                key = '{}{}'.format(self.bot.verbs[verb], self.bot.objects[obj_idx])
                key = key.replace(' ', '')
                self.bot.redis.set('usedKeys', dumps(self.usedKeys))
                return(key)

    @commands.command()
    async def add_rumour(self, ctx, description, gm):
        channel = self.bot.get_channel(RUMOURS)
        newRumour = rumour(self.IDgen(), description, gm, ctx.author)
        msg = await channel.send(embed=newRumour.embed())

        newRumour.eventID = msg.id
        self.rumours.append(newRumour)

        self.bot.redis.set('rumours', dumps(self.rumours))
        return()

    @commands.command(hidden=True)
    async def delete_rumour(self, ctx, id):
        for x in range(0, len(self.rumours)):
            if self.rumours[x].eventID == id:
                channel = self.bot.get_channel(RUMOURS)
                msg = await channel.get_message(self.rumours[x].msgID)
                await msg.delete()
                self.rumours.pop(x)
                self.bot.redis.set('rumours', dumps(self.rumours))
                return()


def setup(bot):
    bot.add_cog(RumoursModule(bot))