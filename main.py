import asyncio
from aiogram import Bot, Dispatcher
from keyboards.set_menu import set_main_menu
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
import logging.config
from loggs import logging_config

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main():
    """
    The function of configuring and launching the bot.
    """
    logger.info('Starting bot')  # Displaying information about the start of the bot launch to the console
    config: Config = load_config()  # Load the configuration
    bot = Bot(token=config.tg_bot.token,  # Initialize the bot
              parse_mode='HTML')
    dp = Dispatcher()  # Initialize the dispatcher
    dp.include_router(user_handlers.router)  # Register routers in the dispatcher
    dp.include_router(other_handlers.router)
    await set_main_menu(bot)  # Set up the main menu button
    await bot.delete_webhook(drop_pending_updates=True)  # Delete any pending updates and start polling
    await dp.start_polling(bot, allowed_updates=[])


if __name__ == '__main__':
    asyncio.run(main())  # Launching the polling
