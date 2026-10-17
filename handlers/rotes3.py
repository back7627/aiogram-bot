from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite

router3 = Router()

# ---

db_name = 'Kiki.sql'

async def init_db():
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,full_name TEXT,age INT);""")
        await db.commit()



async def add_user(full_name, age):
    async with aiosqlite.connect(db_name) as db:
        await db.execute('INSERT INTO users (full_name, age) VALUES(?, ?)', (full_name, age))
        await db.commit()


async def get_users():
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute('SELECT full_name, age FROM users')
        result = await cursor.fetchall()
        return  result

# ---


@router3.message(Command('start'))
async def start(message: Message):
    await init_db()
    await message.answer('Привет!\nПропишите команду: /reg AGE')

@router3.message(Command('reg'))
async def reg(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer('Введите команду верно')
        return
    await add_user(message.from_user.full_name, int(parts[1]))

    await message.answer('Все готово!')

@router3.message(Command('users'))
async def users(message: Message):
    users = await get_users()

    if not users:
        await message.answer('in base no users')
        return
    text = 'Пользователи в базе\n\n'
    for full_name, age in users:
        text += f'- {full_name} - <code>{age}</code>\n'

    await message.answer(text, parse_mode='HTML')