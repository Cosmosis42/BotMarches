from discord.ext import commands
from pickle import loads, dumps
import logging

logging.basicConfig(level=logging.INFO)

class Event:
    def __init__(self, eventID, name, place, date, time, numPlayers, dm, description, msgID, players=None):
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

class EventModule:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.events = loads(self.bot.redis.get('events'))
        except:
            self.events = list()

    @commands.command()
    async def event_add(self, ctx, name, place, date, time, numPlayers, dm, description):
        channel = self.bot.get_channel(483331971771138065)
        eventID = len(self.events)

        output = "**ID: **" + str(eventID)
        output += "\t**Name: **" + name +"\n"
        output += "**Place: **" + place + "\n"
        output += "**Date: **" + date
        output += "\t**Time: **" + time + "\n"
        output += "**Players Needed: " + numPlayers + "\n"
        output += "**DM: **" + dm + "\n"
        output += "**Description: **\n*" + description +"*"

        try:
            msg = await self.bot.send_message(channel, output)
        except:
            logging.info('message not sent.')

        self.events.append(Event(eventID, name, place, date, time, numPlayers, dm, description, msg.id))
        self.bot.redis.set('events', dumps(self.events))

    @commands.command()
    async def event_cancel(self, ctx, eventID):
        for x in self.events:
            if x.eventID == eventID:
                await self.bot.http.delete_message(483331971771138065, x.msgID)
                del x

        self.bot.redis.set('events', dumps(self.events))

def setup(bot):
    bot.add_cog(EventModule(bot))