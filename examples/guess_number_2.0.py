import random
import env

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

BOT_TOKEN = env.BOT_TOKEN
# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 5

# Словарь, в котором будут храниться данные пользователя
users = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Если пользователь только запустил бота и его нет в словаре '
# 'users - добавляем его в словарь.
# Этим декоратором обернём все функции.
def new_user(fn):
    async def wrapper(message: Message):
        if message.from_user.id not in users:
            users[message.from_user.id] = {
                'in_game': False,
                'secret_number': None,
                'attempts': None,
                'total_games': 0,
                'wins': 0
            }
            print(users)
            return await fn(message)
        else:
            print(users)
            return await fn(message)

    return wrapper


# Этот хэндлер будет срабатывать на команду "/stat"
@new_user
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: '
        f'{users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )


# Этот хэндлер будет срабатывать на команду "/start"
@new_user
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )


# Этот хэндлер будет срабатывать на команду "/help"
@new_user
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@new_user
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer('You have exited the game. '
                             'If you want to play again, let us know.')
    else:
        await message.answer("We weren't playing with you anyway. "
                             "Maybe we can play once?")


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@new_user
async def process_positive_answer(message: Message):
    user = users[message.from_user.id]
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, попробуй угадать!')
    else:
        await message.answer('Пока мы играем в игру я могу реагировать только на числа от 1 до 100 и команды /cancel '
                             'и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@new_user
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        response = 'Ээээх((( :(\n\nЕсли захотите поиграть - просто напишите об этом'
    else:
        response = 'Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100'
    await message.answer(response)


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@new_user
async def process_numbers_answer(message: Message):
    user = users[message.from_user.id]

    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer('Ура!!! Вы угадали число!\n\nМожет, сыграем еще?')
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Мое число больше')

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\nМое число '
                f'было {user["secret_number"]}\n\nДавайте сыграем еще?')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@new_user
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        response = 'Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100'
    else:
        response = 'Я довольно ограниченный бот, давайте просто сыграем в игру?'
    await message.answer(response)


dp.message.register(process_start_command, CommandStart())
dp.message.register(process_stat_command, Command(commands='stat'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(process_cancel_command, Command(commands='cancel'))
dp.message.register(process_positive_answer, F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                                                 'играть', 'хочу играть']))
dp.message.register(process_negative_answer, F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
dp.message.register(process_numbers_answer, lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.message.register(process_other_answers)

if __name__ == '__main__':
    dp.run_polling(bot)
