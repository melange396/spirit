import asyncio

import discord

from db.dbase import DBase
from cogs.utils import constants


def delete_all(message):
    """Helper function used to delete messages"""
    return True;


class MessageManager:

    def __init__(self, bot, user, channel, messages=None):
        self.bot = bot
        self.user = user
        self.channel = channel
        if messages:
            self.messages = messages
        else:
            self.messages = []


    async def say_and_wait(self, content, mention=True):
        """Send a message and wait for user's response"""
        def check_res(m):
            return m.author == self.user and m.channel == self.channel

        msg = await self.channel.send("{}: {}".format(self.user.mention, content))
        self.messages.append(msg)
        res = await self.bot.wait_for('message', check=check_res)

        # If the user responds with a command, we'll need to stop executing and clean up
        if res.content.startswith('!'):
            await self.clear()
            return False
        else:
            self.messages.append(res)
            return res


    async def say(self, content, embed=False, delete=True, mention=True):
        """Send a single message"""
        msg = None
        if embed:
            msg = await self.channel.send(embed=content)
        else:
            msg = await self.channel.send("{}: {}".format(self.user.mention, content))
        if delete:
            self.messages.append(msg)


    async def clear(self):
        """Delete messages marked for deletion"""
        def check(message):
            if (message.author in (self.user, self.bot.user)
                and message.id in [m.id for m in self.messages]):
                return True

        if not isinstance(self.channel, discord.abc.PrivateChannel):
            await asyncio.sleep(constants.SPAM_DELAY)
            await self.channel.purge(limit=999, check=check)
