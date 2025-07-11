from discord import app_commands
from datetime import datetime
import logging

from bot.utils.log_setup import setup_logging

# log 初始化
setup_logging()
logger = logging.getLogger(__name__)

def to_datetime(datetime_str: str, format: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    return datetime.strptime(datetime_str, format)

def current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def current_datetime_obj() -> datetime:
    return datetime.now()