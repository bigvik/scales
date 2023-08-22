import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from abc import ABC, abstractmethod
import threading
import time

import control
import config
import test

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()
chat_id = 0
buffer = []

class BotObserver(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:

        pass


def msg(subject):
    buffer.append(subject)

class BotListener(BotObserver):
    '''Конкретный слушатель'''

    def update(self, subject):
        msg(subject)

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Hello! Chat_Id: {chat_id}")
    test.test_bot()
    #test()


# async def process_messages(queue):
#     while True:
#         message = await queue.get()
#         await bot.send_message(chat_id, message)


""" def test():
    for x in range(10):
        bot.send_message(chat_id, x)
        time.sleep(3) """

async def main():
    # queue = asyncio.Queue()
    # asyncio.ensure_future(process_messages(queue))
    #await asyncio.sleep(1)
    await dp.start_polling(bot)

if __name__ == "__main__":
    
    lister = BotListener()
    control.anons.attach(lister)
    asyncio.run(main())