import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from abc import ABC, abstractmethod

import control
import config


class BotObserver(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:
        pass


class BotListener(BotObserver):
    '''Конкретный слушатель'''

    def update(self, subject):
        msg(subject)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"CHAT ID: {update.effective_chat.id}!")

def msg(subject):
    print(f'BOT SAY: {subject}')


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    lister = BotListener()
    control.anons.attach(lister)
    
    application.run_polling()