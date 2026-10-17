import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from handlers.routes import router
from handlers.routes2 import router2
from handlers.rotes3 import router3
from handlers.router4 import router, notifier

load_dotenv()
TOK = getenv('BOT_TOKEN')

dp = Dispatcher()
dp.include_router(router)

async def main():
    session = AiohttpSession(
        api=TelegramAPIServer.from_base("https://frosty-mud-556a.thevest141516.workers.dev")
    )
    bot = Bot(token=TOK, session=session)

    asyncio.create_task(notifier(bot))

    print('Start...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# вырузка
# pip freeze > requirements.txt
# git init
# .gitignore и добавляем .env
# git add .
# git commit -m "first commit"