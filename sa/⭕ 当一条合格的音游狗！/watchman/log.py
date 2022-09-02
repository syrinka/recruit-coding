from loguru import logger
from .config import config

stat_filter = lambda x: x['extra'].get('stat', False)


for handler in config['log']['console']:
    logger.add(**handler)


for handler in config['log']['stat']:
    logger.add(**handler, filter=stat_filter, level=5)
