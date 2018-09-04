from discord import Embed, Colour
from discord.ext import commands
from pickle import loads, dumps
import logging
from textwrap import dedent

logging.basicConfig(level=logging.INFO)

SCHEDULING = 483331971771138065
class Event:
    def __init__(self, eventID, name, place, date, time, numPlayers, dm, description, msgID=None, players=None):
        self.eventID = eventID
        self.name = name
        self.place = place
        self.date = date
        self.time = time
        self.numPlayers = numPlayers
        self.dm = dm
        self.description = description
        self.msgID = msgID
        self.players = players

    def __str__(self):
        output = """
        **ID:** {self.eventID}\t**Name:** {self.name}
        **Place:** {self.place}
        **Date:** {self.date}\t**Time:** {self.time}
        **Players Needed:** {self.numPlayers}
        **DM:** {self.dm}
        **Description:**
        *{self.description}*
        """.format(self=self)
        output = dedent(output)

        return(output)

    def embed(self):
        temp = Embed(
            title=self.eventID,
            type='rich',
            author='Corbin',
            colour=Colour.from_rgb(23, 160, 101)
        )

        temp.add_field(name='**ID:**', value=self.eventID)
        temp.add_field(name='**Name:**', value=self.name)
        temp.add_field(name='**Place:**', value=self.place, inline=False)
        temp.add_field(name='**Date:**', value=self.date, inline=False)
        temp.add_field(name='**Time:**', value=self.time)
        temp.add_field(name='**Players Needed:**', value=self.numPlayers, inline=False)
        temp.add_field(name='**DM:**', value=self.dm, inline=False)
        temp.add_field(name='**Description:**', value=self.description, inline=False)

        return(temp)

class EventModule:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.events = loads(self.bot.redis.get('events'))
        except:
            self.events = list()

    @commands.command()
    async def event_add(self, ctx, name, place, date, time, numPlayers, dm, description):
        channel = self.bot.get_channel(SCHEDULING)
        eventID = len(self.events)
        NewEvent = Event(eventID, name, place, date, time, numPlayers, dm, description)
        
        msg = await channel.send(embed=NewEvent.embed())

        NewEvent.msgID = msg.id
        self.events.append(NewEvent)

        self.bot.redis.set('events', dumps(self.events))

    @commands.command()
    async def event_cancel(self, ctx, eventID : int):
        for x in self.events:
            if x.eventID == eventID:
                channel = self.bot.get_channel(SCHEDULING)
                msg = await channel.get_message(x.msgID)
                await msg.delete()
                self.events.pop(x)

        self.bot.redis.set('events', dumps(self.events))

def setup(bot):
    bot.add_cog(EventModule(bot))