import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from abc import ABC, abstractmethod
import threading

import control, test

bot = Bot('6426144545:AAFTPiA6k4aSQaY0flxbg1q5DDCFJnuT--s')
dp = Dispatcher()
chat_id = 0

class Observer(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:

        pass


class Listener(Observer):
    '''Конкретный слушатель'''

    def update(self, subject):
        bot.send_message(chat_id, subject)

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Hello! Chat_Id: {chat_id}")
    test.test_bot()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    lister = Listener()
    control.anons.attach(lister)