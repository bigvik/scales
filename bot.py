import telebot
import logging
from abc import ABC, abstractmethod

import control
import config
import test

bot = telebot.TeleBot(config.BOT_TOKEN)
cid = 0


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    cid = message.chat.id
    bot.reply_to(message, f"Howdy, how are you doing {cid}?")
    bot.send_message(cid,"Привет ✌️ ")
        
def send_msg(sub):
     bot.send_message(chat_id=cid, text=sub)


class BotObserver(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:

        pass


class BotListener(BotObserver):
    '''Конкретный слушатель'''

    def update(self, subject):
        send_msg(subject)


if __name__ == "__main__":
    
    lister = BotListener()
    control.anons.attach(lister)

    bot.infinity_polling()