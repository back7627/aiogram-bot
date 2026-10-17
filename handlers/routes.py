from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (Message,
                           CallbackQuery,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

router = Router()


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='/about')],
            [KeyboardButton(text='Старт'), KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard= [
            [InlineKeyboardButton(text='Открыть сайт', url='https://youtube.com')],
            [InlineKeyboardButton(text='Подробнее', callback_data='info_more')]
        ]
    )
    return keyboard


@router.callback_query(lambda c: c.data == 'info_more')
async def proccess_more_info(callback):
    await callback.message.answer('Вот более подробная информация')
    await callback.answer()

@router.message(Command('start'))
@router.message(F.text.lower() == 'старт')
async def start(message: Message):
    await message.answer('*Hello!*, я простой бот _для_ тебя\n\nНапиши /help для помощи', parse_mode='Markdown')

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Команды:\n<b>/start</b> - запустить бот\n<i>/help</i> - список <a href="https://google.com">команд</a>\n/about - о боте',
                         parse_mode='HTML',
                         reply_markup=get_main_reply_keyboard())

@router.message(Command('about'))
async def about(message: Message):
    await message.answer(f'Это команда про бота. Твое имя: {message.from_user.first_name}', reply_markup=get_main_inline_keyboard())


@router.message()
async def mess(message: Message):
    await message.answer('text message')