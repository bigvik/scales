import telebot
import logging
from abc import ABC, abstractmethod

import control
import config
import test

bot = telebot.TeleBot(config.BOT_TOKEN)
cid = 0

@bot.message_handler(commands=['test'])
def testing(message):
    s = False
    for k, v in config.CHAT_IDS.values():
        send_msg(message.chat.id, f"{k} - {v}")
        if v == message.chat.id:
            s = True
    if s:
        test.test_bot()
    else:
        bot.reply_to(message, f"У вас ({message.chat.id}) не достаточно прав")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    s = False
    for k, v in config.CHAT_IDS.values():
        send_msg(message.chat.id, f"{k} - {v}")
        if v == message.chat.id:
            s = True
    if s:
        bot.reply_to(message, f"Привет, {k}")
    else:
        bot.reply_to(message, f"У вас ({message.chat.id}) не достаточно прав")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if val := config.CHAT_IDS.get(message.text):
        bot.reply_to(message, f"Привет, {val[0]}")
    else:
        bot.reply_to(message, f"Сообщение не распознано {message}")

def send_msg(cid, sub):
     bot.send_message(chat_id=cid, text=sub)


class BotObserver(ABC):
    '''Абстрактный слушатель'''

    @abstractmethod
    def update(self, subject) -> None:

        pass


class BotListener(BotObserver):
    '''Конкретный слушатель'''

    def update(self, subject):
        if subject[0]:
            for k, v in config.CHAT_IDS.values():
                send_msg(v, subject[0])


if __name__ == "__main__":
    
    lister = BotListener()
    control.anons.attach(lister)

    bot.infinity_polling()