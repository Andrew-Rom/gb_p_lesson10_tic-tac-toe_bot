import telebot
from telebot import types
from os import getenv
from sys import exit
import logger as lg

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = telebot.TeleBot(token=bot_token)

tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player = 1
step_counter = 0


def playfield(data_tab):
    a = '----------------\n'
    for i in range(3):
        a += f'  {data_tab[0 + i * 3]} | {data_tab[1 + i * 3]} | {data_tab[2 + i * 3]}  \n----------------\n'
    return a


def who_won(data_steps):
    winner_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], \
                    [0, 3, 6], [1, 4, 7], [2, 5, 8], \
                    [0, 4, 8], [2, 4, 6]]
    for j in winner_lines:
        if data_steps[j[0]] == data_steps[j[1]] == data_steps[j[2]]:
            return data_steps[j[0]]
    return False


def is_valid_step(value, data_tab):
    return 1 <= value <= 9 and data_tab[value - 1] != "X" and data_tab[value - 1] != "O"


@bot.message_handler(commands=['start'])
def start(message):
    global tab
    bot.send_message(message.chat.id, "Hello! I'm andy_bot.\n"
                                      "Let's play tic-tac-toe game")
    bot.send_message(message.chat.id, 'The /game started')
    bot.send_message(message.chat.id, f'{playfield(tab)}')


@bot.message_handler(commands=['game'])
def number(message):
    global player
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('1')
    button2 = types.KeyboardButton('2')
    button3 = types.KeyboardButton('3')
    button4 = types.KeyboardButton('4')
    button5 = types.KeyboardButton('5')
    button6 = types.KeyboardButton('6')
    button7 = types.KeyboardButton('7')
    button8 = types.KeyboardButton('8')
    button9 = types.KeyboardButton('9')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
    bot.send_message(message.chat.id, f"Player {player}, select a gamefield's number", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def select_position(message):
    if message.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        set_symbol(message)
    else:
        bot.send_message(message.chat.id, 'Please, click button')
        number(message)


def set_symbol(message):
    global player, step_counter, tab
    pos = int(message.text)
    if player == 1 and step_counter < 9:
        step = 'X'
        if is_valid_step(pos, tab):
            tab[pos - 1] = step
            bot.send_message(message.chat.id, f'{playfield(tab)}')
            step_counter += 1
            player = 2
            if who_won(tab) == False:
                number(message)
            elif step_counter >= 9:
                bot.send_message(message.chat.id, 'The game finished.\nDrawn game.')
                tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                step_counter = 0
                bot.send_message(message.chat.id, 'Press /start to try again')
            else:
                bot.send_message(message.chat.id, 'The game finished')
                winner = who_won(tab)
                if winner == 'X':
                    bot.send_message(message.chat.id, 'Player 1 won.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Press /start to try again')
                elif winner == "O":
                    bot.send_message(message.chat.id, 'Player 2 won.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Press /start to try again')
        else:
            bot.send_message(message.chat.id, 'This cell is already occupied')
            number(message)
    elif player == 2 and step_counter < 9:
        step = 'O'
        if is_valid_step(pos, tab):
            tab[pos - 1] = step
            bot.send_message(message.chat.id, f'{playfield(tab)}')
            step_counter += 1
            player = 1
            if who_won(tab) == False:
                number(message)
            elif step_counter >= 9:
                bot.send_message(message.chat.id, 'The game finished.\nDrawn game.')
                tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                step_counter = 0
                bot.send_message(message.chat.id, 'Press /start to try again')
            else:
                bot.send_message(message.chat.id, 'The game finished')
                winner = who_won(tab)
                if winner == 'X':
                    bot.send_message(message.chat.id, 'Player 1 won.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Press /start to try again')

                elif winner == "O":
                    bot.send_message(message.chat.id, 'Player 2 won.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Press /start to try again')

        else:
            bot.send_message(message.chat.id, 'This cell is already occupied')
            number(message)

bot.infinity_polling()
