import telebot
from telebot import types
from os import getenv
from sys import exit
import logger as lg

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I'm andy_bot.\n"
                                      "I can help you with some simple math /operation")


bot.infinity_polling()
