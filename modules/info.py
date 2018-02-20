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
import platform
import asyncio

class InfoModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, user:discord.User=None):
        """Grab information about a user"""
        if not ctx.message.guild:
            return await ctx.send("You can only execute this command in a guild")
        guild = ctx.message.guild
        if not user:
            user = ctx.author
        member = guild.get_member(user.id)
        _roles = member.roles
        roles = []
        for role in _roles:
            roles.append(role.name.replace("@here", "[at]here").replace("@everyone", "[at]everyone"))
        embed = discord.Embed(color=discord.Colour.green())
        embed.title = "{}#{}".format(user.name, user.discriminator)
        if user.id in self.bot.config.admins:
            embed.title += " <:dev:415580034280194049>"
        joined_at = member.joined_at
        since_joined = (ctx.message.created_at - joined_at).days
        since_created = (ctx.message.created_at - user.created_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        joined_at = joined_at.strftime("%d %b %Y %H:%M")
        embed.add_field(name="ID", value="{}".format(user.id), inline=True)
        embed.add_field(name="Username", value="{}".format(user.name), inline=True)
        embed.add_field(name="Game", value=member.game, inline=True)
        embed.add_field(name="Roles", value=", ".join(roles))
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Created At", value="{} (Thats over {} days ago)".format(user_created, since_created), inline=True)
        embed.add_field(name="Joined At", value="{} (Thats over {} days ago)".format(joined_at, since_joined), inline=True)
        return await ctx.send(embed=embed)

    @commands.command(aliases=["info","botinfo"])
    async def about(self, ctx):
        """Get more information about the bot"""
        bot = self.bot
        if not hasattr(bot, "owner"):
            return await ctx.send("Hey, I'm sorry, but the bot is not ready yet, please try again in a few seconds.")
        embed = discord.Embed(color=discord.Colour.green())
        discord_version = discord.__version__
        python_version = platform.python_version()
        embed.add_field(name="Discord.py Version", value=discord_version, inline=True)
        embed.add_field(name="Python Version", value=python_version, inline=True)
        embed.add_field(name="Author", value=bot.owner.owner, inline=True)
        embed.add_field(name="Latency", value=str(round(bot.latency, 3)), inline=True)
        embed.add_field(name="Guilds", value=str(len(bot.guilds)), inline=True)
        embed.add_field(name="Users", value=str(len(bot.users)), inline=True)
        if ctx.message.guild:
            embed.add_field(name="Shard ID", value=str(ctx.message.guild.shard_id), inline=True)
        embed.add_field(name="Links", value="**[GitHub Link]({links.github})\n[Guild Invite]({links.serverinvite})\n[Bot Invite]({links.botinvite})**".format(links=self.bot.config.links))
        embed.add_field(name="Developers", value="{}".format(bot.owner.owner))
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(InfoModule(bot))