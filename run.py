# Setup logging
import logging,logging.handlers,sys;FORMAT='[%(levelname)s] [%(name)s] [%(asctime)s]: %(message)s';logger=logging.getLogger("RandomBot");format=logging.Formatter(FORMAT, datefmt="%d/%m/%Y %H:%M");stdout_handler=logging.StreamHandler(sys.stdout);stdout_handler.setFormatter(format);fhandler=logging.handlers.RotatingFileHandler(filename='main.log',encoding='utf-8',mode='a',maxBytes=10**7,backupCount=5);fhandler.setFormatter(format);logger.addHandler(stdout_handler);logger.addHandler(fhandler)

"""
    RandomBot
    Copyright (C) 2018 JustMaffie

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Try to use uvloop if available
try:
    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    # UVLoop can't be imported, it probably isn't installed, you are probably on Windows, UVLoop is optional but recommended for production instances
    logger.warn("UVLoop can't be imported, its recommended to install UVLoop for a production instance, you can safely ignore this message.")
    logger.setLevel(logging.INFO)

from randombot import make_bot

bot = make_bot(logger)

try:
    bot.run_bot()
except KeyboardInterrupt:
    bot.shutdown()