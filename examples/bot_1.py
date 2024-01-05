import env
import requests
import time
import asyncio
from aiogram import Bot, Dispatcher, types, filters, F
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters import Command, MagicData
import json

API_URL = env.API_URL
BOT_TOKEN = env.BOT_TOKEN
# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ----------------------echo-bot-1---------------------------------------------------------

# Этот хэндлер будет срабатывать на команду "/command1"
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/command2"
async def process_help_command(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

# Этот хэндлер будет срабатывать на отправку боту фото


async def send_photo_echo(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply_photo(message.photo[0].file_id)


# Этот хэндлер будет срабатывать на отправку видео
async def send_video_echo(message: Message):
    await message.answer_video(message.video.file_id)


# Этот хэндлер будет срабатывать на отправку видео сообщений
async def send_video_note_echo(message: Message):
    await message.answer_video_note(message.video_note.file_id)


# Этот хэндлер будет срабатывать на отправку стикеров
async def send_sticker_echo(message: Message):
    await message.answer_sticker(message.sticker.file_id)


# Этот хэндлер будет срабатывать на отправку аудио файлов
async def send_audio_echo(message: Message):
    await message.answer_audio(message.audio.file_id)


# Этот хэндлер будет срабатывать на отправку голосовых сообщений
async def send_voice_echo(message: Message):
    await message.answer_voice(message.voice.file_id)


# Этот хэндлер будет срабатывать на отправку любых файлов
async def send_files(message: Message):
    await message.answer_document(message.document.file_id)


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения, кроме команд "/start" и "/help"
async def send_echo(message: Message):
    print(message)
    await message.reply(message.text)


# Регистрируем хэндлеры
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_video_echo, F.video)
dp.message.register(send_video_note_echo, F.video_note)
dp.message.register(send_sticker_echo, F.sticker)
dp.message.register(send_audio_echo, F.audio)
dp.message.register(send_voice_echo, F.voice)
dp.message.register(send_files, F.document)
dp.message.register(process_start_command, Command(commands='command1'))
dp.message.register(process_help_command, Command(commands='command2'))
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)

# ----------------------echo-bot---------------------------------------------------------

# # Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(Command(commands=["command1"]))
# async def process_start_command(message: Message):
#     await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')
#
#
# # Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=['command2']))
# async def process_help_command(message: Message):
#     await message.answer(
#         'Напиши мне что-нибудь и в ответ '
#         'я пришлю тебе твое сообщение')
#
#
# # Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# # кроме команд "/start" и "/help"
# @dp.message()
# async def send_echo(message: Message):
#     await message.reply(text=message.text)
#
#
#
# if __name__ == '__main__':
#     dp.run_polling(bot)

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
