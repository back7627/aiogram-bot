from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (Message,
                           CallbackQuery,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from forms.user import Form
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import FSInputFile
router2 = Router()

@router2.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Давайте начнем заполнять вашу анкету!\nСперва введите ваше имя:')
    await state.set_state(Form.name)

@router2.message(Command('cancel'))
async def cancel_form(message:Message, state: FSMContext):
    await state.clear()
    await message.answer('Анкета отклонена!')

@router2.message(Form.name, F.text)
async def proccess_name(message:Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Отлично!\nА теперь введите ваш возраст:')
    await state.set_state(Form.age)


@router2.message(Form.age, F.text)
async def proccess_age(message:Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Возраст должен быть числом!')
        return

    if int(message.text) < 1 or int(message.text) > 100:
        await message.answer('Возраст должен быть от 1 до 100!!')
        return

    await state.update_data(age=int(message.text))

    await message.answer('Прекрасно!\nА теперь введите ваш email:')
    await state.set_state(Form.email)

@router2.message(Form.email, F.text)
async def proccess_email(message:Message, state: FSMContext):
    email_text = message.text
    if '@' not in email_text or '.' not in email_text:
        await message.answer('Неправильно введен email-адрес')
        return

    await state.update_data(email=email_text)

    data = await state.get_data()
    name = data['name']
    age = data['age']
    email = data['email']

    await message.answer(f'Анкета готова!\nИмя: {name}\n'
                         f'Возраст: {age}\n'
                         f'Почта: {email}')
    await state.clear()


@router2.message(F.photo)
async def proccess_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(f'Вы отправили фото!\nID photo: <code>{file_id}</code>', parse_mode='HTML')

    await message.answer_photo(file_id, caption='Вот ваше фото!')

@router2.message(F.video)
async def proccess_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer(f'Вы отправили видео!'
                         f'\nID video: <code>{file_id}</code>'
                         f'\nДлительность: <code>{duration}</code>', parse_mode='HTML')

    await message.answer_video(file_id, caption='Вот ваше видео!')

@router2.message(F.animation)
async def proccess_animation(message: Message):
    animation = message.animation

    await message.answer(f'Вы отправили animation!'
                         f'\nID animation: <code>{animation.file_id}</code>'
                         , parse_mode='HTML')

    await message.answer_video(animation.file_id, caption='Вот ваше animation!')

@router2.message(F.document)
async def proccess_document(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f'downloads/{document.file_name}'

    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer('Файл сохранен!')

@router2.message(Command('file'))
async def send_file(message: Message):
    file = FSInputFile('files/example.txt')
    await message.answer_document(file)