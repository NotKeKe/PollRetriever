from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class CogExtension(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot