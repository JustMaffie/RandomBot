"""
    RandomBot
    Copyright (C) 2018 JustMaffie

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from discord.ext import commands
import discord
import logging
import traceback
import time

class EventsModule:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        millis = int(round(time.time() * 1000))
        bot = self.bot
        game = discord.Game(name="with random API's")
        await bot.change_presence(status=discord.Status.online, game=game)
        self.bot.owner = await self.bot.application_info()
        info = ["", str(self.bot.user), "Discord.py version: {}".format(discord.__version__), 'Shards: {}'.format(self.bot.shard_count), 'Guilds: {}'.format(len(self.bot.guilds)),
            'Users: {}'.format(len(set([m for m in self.bot.get_all_members()]))), '{} modules with {} commands'.format(len(self.bot.cogs), len(self.bot.commands)),
            "Owner: {}".format(str(self.bot.owner.owner)), "Startup duration: {}ms".format(millis - bot.startup_time)]
        for string in info:
            self.bot.logger.info(string)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help()
        elif isinstance(error, commands.BadArgument):
            await ctx.send_help()
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("It looks like this command is disabled.")
        elif isinstance(error, commands.CommandInvokeError):
            logging.exception("An error occurred in the command '{}'"
                          "".format(ctx.command.qualified_name), exc_info=error.original)
            message = ("An error occurred in the command ``{}``. Please contact the bot admins ASAP."
                       "".format(ctx.command.qualified_name))
            await ctx.send(message)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Hey, I'm sorry, but I can't let you do that")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Could I ask you to move to a guild?")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown. "
                           "Try again in {:.2f}s"
                           "".format(error.retry_after))
        else:
            traceback.print_exc()
def setup(bot):
    bot.add_cog(EventsModule(bot))