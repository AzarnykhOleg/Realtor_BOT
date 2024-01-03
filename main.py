import env
import requests
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters import Command


API_URL = env.API_URL
BOT_TOKEN = env.BOT_TOKEN

# ----------------------echo-bot---------------------------------------------------------

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["command1"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['command2']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)

# ----------------------long pooling---------------------------------------------------------

# offset = -2
# timeout = 60
# updates: dict
#
#
# def do_something() -> None:
#     print('Был апдейт')
#
#
# while True:
#     start_time = time.time()
#     updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
#
#     if updates['result']:
#         for result in updates['result']:
#             offset = result['update_id']
#             do_something()
#
#     end_time = time.time()
#     print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')

# -------------------------------------------------------------------------------

# TEXT = 'Ура! Классный апдейт!'
# MAX_COUNTER = 100
#
# offset = -2
# counter = 0
# chat_id: int
# text: str

# while counter < MAX_COUNTER:
#
#     print('attempt =', counter)  #Чтобы видеть в консоли, что код живет
#
#     updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
#
#     if updates['result']:
#         for result in updates['result']:
#             offset = result['update_id']
#             chat_id = result['message']['from']['id']
#             text = result['message']['text']
#             print(f'offset = {offset}, chat_id = {chat_id}, text = {text}')
#             requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
#
#     time.sleep(1)
#     counter += 1

# -------------------------------update with cats------------------------------------------------


# await message.answer("Some text here", reply_markup=builder.as_markup())


# API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
# ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
#
# offset = -2
# counter = 0
# cat_response: requests.Response
# cat_link: str
#
# while counter < 100:
#     print('attempt =', counter)
#     updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
#
#     if updates['result']:
#         for result in updates['result']:
#             offset = result['update_id']
#             chat_id = result['message']['from']['id']
#             cat_response = requests.get(API_CATS_URL)
#             if cat_response.status_code == 200:
#                 cat_link = cat_response.json()[0]['url']
#                 requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
#             else:
#                 requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
#
#     time.sleep(1)
#     counter += 1

# -------------------------------------------------------------------------------
