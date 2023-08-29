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
    if val := config.CHAT_IDS.get(message.text):
        test.test_bot()
    else:
        bot.reply_to(message, f"У вас не достаточно прав")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global cid
    cid = message.chat.id
    if cid == 169695840:
        bot.reply_to(message, "Введите ваш PIN:")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if val := config.CHAT_IDS.get(message.text):
        bot.reply_to(message, f"Привет, {val[0]}")
    else:
        bot.reply_to(message, f"Сообщение не распознано {message}")

def send_msg(sub):
     global cid
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
            print(subject[0])
            send_msg(subject[0])


if __name__ == "__main__":
    
    lister = BotListener()
    control.anons.attach(lister)

    bot.infinity_polling()