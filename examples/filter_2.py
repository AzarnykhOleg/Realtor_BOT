from typing import List

import env

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, BaseFilter
from aiogram.types import Message

BOT_TOKEN = env.BOT_TOKEN
# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот фильтр будет проверять наличие неотрицательных чисел
# в сообщении от пользователя, и передавать в хэндлер их список
class NumbersInMessage(BaseFilter):
    """
    Asynchronously processes a message and extracts a list of numbers from the message text.

    Args:
        message (Message): The message object to process.

    Returns:
        Union[bool, dict[str, List[int]]]: If numbers are found in the message text, returns a dictionary
            with the numbers list as the value. Otherwise, returns False.
    """

    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:

        # Initialize an empty list to store numbers
        numbers: list[int] = []
        # Split the message by spaces to get individual words
        for word in message.text.split():
            # Normalize each word by removing punctuation and whitespace
            normalized_word = word.replace('.', '').replace(',', '').strip()
            # Check if the normalized word consists only of digits
            if normalized_word.isdigit():
                # Convert the normalized word to an integer and add it to the numbers list
                numbers.append(int(normalized_word))

        # If there are numbers in the list, return a dictionary with the numbers list as the value
        if numbers:
            return {'numbers': numbers}

        # If there are no numbers, return False
        return False


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа" и в нем есть числа
@dp.message(F.text.lower().startswith('найди числа'),
            NumbersInMessage())
# Помимо объекта типа Message, принимаем в хэндлер список чисел из фильтра
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(
        text=f'Нашел: {", ".join(str(num) for num in numbers)}')


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа", но в нем нет чисел
@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(
        text='Не нашел что-то :(')

if __name__ == '__main__':
    dp.run_polling(bot)