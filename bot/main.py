import discord
from discord.ext import commands
import logging
from datetime import datetime
import asyncio
from pathlib import Path

from bot.utils.log_setup import setup_logging
from config import BOT_TOKEN

# log 初始化
setup_logging()
logger = logging.getLogger(__name__)

class MyBot(commands.Bot):  
    def __init__(self):   
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(  
            command_prefix=']',  
            intents=intents,  
        )  
          
    async def on_ready(self):  
        print(f'Bot is ready! Logged in as {self.user}') 

    async def setup_hook(self):
        cogs_path = Path("bot/cogs")
        for file in cogs_path.glob("*.py"):
            if file.name == "__init__.py": continue

            try:
                await self.load_extension(f"bot.cogs.{file.stem}")
            except:
                logger.error(f'Error when loading {file.stem}', exc_info=True)

        await self.tree.sync()

    async def on_ready(self):
        logger.info(f'{self.user} 在 `{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}` 上線了窩w')

bot = MyBot()


async def main():
    async with bot:
        await bot.start(BOT_TOKEN)

asyncio.run(main())