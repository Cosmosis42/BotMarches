from discord import Embed, Colour
from discord.ext import commands
from pickle import loads, dumps
import logging
from textwrap import dedent
from random import randint

logging.basicConfig(level=logging.INFO)

SCHEDULING = 483331971771138065

def blank_event():
    tempEvent = Event(
        eventID=None,
        name=None,
        place=None,
        date=None,
        time=None,
        numPlayers=None,
        dm=None,
        description=None
    )
    return(tempEvent)

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
            title='ID: {}'.format(self.eventID),
            type='rich',
            author='Corbin',
            colour=Colour.from_rgb(23, 160, 101)
        )

        #temp.add_field(name='**ID:**', value=self.eventID)
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
        
        try:
            self.usedKeys = loads(self.bot.redis.get('usedKeys'))
        except:
            self.usedKeys = list()

    def IDgen(self):
        while True:
            adj_idx = randint(0, len(self.bot.adjectives))
            an_idx = randint(0, len(self.bot.animals))
            key_tup = (adj_idx, an_idx)
            if key_tup not in self.usedKeys:
                self.usedKeys.append(key_tup)
                key = '{}{}'.format(self.bot.adjectives[adj_idx], self.bot.animals[an_idx])
                key = key.replace(' ', '')
                self.bot.redis.set('usedKeys', dumps(self.usedKeys))
                return(key)

    @commands.command()
    async def event_add(self, ctx, name, place, date, time, numPlayers, dm, description):
        channel = self.bot.get_channel(SCHEDULING)
        eventID = self.IDgen()
        NewEvent = Event(eventID, name, place, date, time, numPlayers, dm, description)
        
        msg = await channel.send(embed=NewEvent.embed())

        NewEvent.msgID = msg.id
        self.events.append(NewEvent)

        self.bot.redis.set('events', dumps(self.events))

    @commands.command()
    async def event_cancel(self, ctx, eventID):
        if eventID.isdigit():
            eventID = int(eventID)
        for x in range(0, len(self.events)):
            if self.events[x].eventID == eventID:
                channel = self.bot.get_channel(SCHEDULING)
                msg = await channel.get_message(self.events[x].msgID)
                await msg.delete()
                self.events.pop(x)
                self.bot.redis.set('events', dumps(self.events))
                return()

    @commands.command(hidden=True)
    async def event_dump(self, ctx):
        channel = self.bot.get_channel(SCHEDULING)
        for entry in range(0, len(self.events)):
            msg = await channel.send(embed=self.events[entry].embed())
            self.events[entry].msgID = msg.id
            
        self.bot.redis.set('events', dumps(self.events))

    @commands.command()
    async def event_wizard(self, ctx):
        newEvent = blank_event()
        channel = await ctx.author.create_dm()

        def check(message):
            return(message.channel==channel)

        await channel.send('Event Name?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.name = reply.content
        await channel.send('Place?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.place = reply.content
        await channel.send('Date?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.date = reply.content
        await channel.send('Time?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.time = reply.content
        await channel.send('Number of players?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.numPlayers = reply.content
        await channel.send('Dungeon Master?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.dm = reply.content
        await channel.send('Description?')
        reply = await self.bot.wait_for('message', check=check)
        newEvent.Description = reply.content

        newEvent.eventID = self.IDgen()
        msg = await channel.send(embed=newEvent.embed())

        newEvent.msgID = msg.id
        self.events.append(newEvent)

        self.bot.redis.set('events', dumps(self.events))
        return()







def setup(bot):
    bot.add_cog(EventModule(bot))