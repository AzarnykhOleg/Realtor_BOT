from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_COMMANDS_RU


async def set_main_menu(bot: Bot):
    """
    Set the main menu commands for the bot.

    Args:
        bot: The bot instance.

    Returns:
        None
    """
    # Create a list of BotCommand objects using a list comprehension.
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    # Set the main menu commands for the bot.
    await bot.set_my_commands(main_menu_commands)