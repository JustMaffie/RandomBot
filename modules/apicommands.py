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
import aiohttp

class APICommandsModule:
    def __init__(self, bot):
        self.bot = bot

    async def get_session(self):
        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession()
        return self.session

    async def get(self, api_url):
        session = await self.get_session()
        resp = await session.get(api_url)
        content = await resp.json()
        resp.close()
        return content

    async def get_file(self, file_url):
        session = await self.get_session()
        resp = await session.get(file_url)
        data = await resp.read()
        resp.close()
        return data

    @commands.command()
    async def trbmb(self, ctx):
        await ctx.trigger_typing()
        quote = await self.get("http://api.chew.pro/trbmb")
        return await ctx.send("``{}``".format(quote[0]))

    @commands.command()
    async def whatdoestrumpthink(self, ctx):
        await ctx.trigger_typing()
        quote = await self.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random")
        return await ctx.send("``{}``".format(quote['message']))

    @commands.command()
    async def dog(self, ctx):
        await ctx.trigger_typing()
        dog = await self.get("https://dog.ceo/api/breeds/image/random")
        img = await self.get_file(dog['message']) # Download the image
        file = discord.File(img, "dog.png")
        return await ctx.send(file=file)


def setup(bot):
    bot.add_cog(APICommandsModule(bot))