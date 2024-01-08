from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import game_kb, yes_no_kb, keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.services_game_1 import get_bot_choice, get_winner

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(Command(commands='start_game_1'))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start_game_1'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help_game_1'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help_game_1'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(F.text.in_([LEXICON_RU['rock'],
                            LEXICON_RU['paper'],
                            LEXICON_RU['scissors']]))
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)

    # Этот хэндлер будет срабатывать на команду "/start"
    # и отправлять в чат клавиатуру с инлайн-кнопками


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Это инлайн-кнопки. Нажми на любую!',
        reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed' или 'big_button_2_pressed'
@router.callback_query(F.data.in_(['big_button_1_pressed',
                                   'big_button_2_pressed']))
async def process_buttons_press(callback: CallbackQuery):
    await callback.answer()
