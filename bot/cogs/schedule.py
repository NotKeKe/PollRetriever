import discord
from discord import app_commands
from discord.ext import commands
import logging 

from bot.src.datebases import Schedule as db
from bot.src.ai.chat import str_to_time
from bot.utils.classes import CogExtension

logger = logging.getLogger(__name__)

class Schedule(CogExtension):
    async def cog_load(self):
        logger.info('Schedule Cog loaded')    

    @app_commands.command(name='schedule', description='建立一個排程')
    @app_commands.describe(event='事件名稱', description='事件描述 (可在此輸入你要補充的資訊，最後會一起傳送)', )
    async def schedule(self, inter: discord.Interaction, event: str, descrip: str, vote_end_time: str):
        time = await str_to_time(vote_end_time)
        db.init_schedule(inter.message.id, event, time, descrip)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Schedule(bot))