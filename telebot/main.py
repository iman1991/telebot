#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import settings
import inDB
import handlers
import socket
import json


bot = telebot.TeleBot(settings.token)

text_welcome = settings.text_welcome

text_get = settings.text_get

text_id = settings.text_id

text_error = settings.text_error

back_menu_list = settings.back_menu_list

main_menu_list = settings.main_menu_list



@bot.message_handler(commands=['start'])
def handle_start(message):
    handlers.answer_text(message, text_welcome, handlers.generator_menu(message, main_menu_list))

@bot.message_handler(regexp='Получить воду')
def handle_start(message):
    sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
    # global infuser
    # infuser['method'] = 'GetWater'
    bot.register_next_step_handler(sent, check)

@bot.message_handler(regexp='Пополнить баланс')
def handle_start(message):
    sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
    bot.register_next_step_handler(sent, check)

@bot.message_handler(regexp='Баланс')
def handle_start(message):
    answer_text(message, "{}₽".format(get_score(message)), handlers.generator_menu(message, back_menu_list))

@bot.message_handler(regexp='Назад')
def handle_start(message):
    handlers.answer_text(message, text_get, handlers.generator_menu(message, main_menu_list))




def get_score(message):
    uid = message.from_user.id
    res = inDB.score(uid)
    return res



def check(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    res = inDB.score(uid)
    user_markup = telebot.types.ReplyKeyboardMarkup()
    if message.text.isdigit():
        # global infuser
        # infuser['param']['idv'] = int(message.text)
        # infuser['param']['idT'] = message.from_user.id
        # infuser['param']['score'] = res
        bot.send_message(message.from_user.id, '1 литр 4₽\nПоднесите тару к водомату и нажмите кноку "Старт" на аппарате.', reply_markup=user_markup)
        # j = json.dumps(infuser)
        # sock.send(j.encode("utf-8"))
        # data = sock.recv(2048)
    elif not (message.text.isdigit()) and not "Назад":
        bot.send_message(message.from_user.id, 'Ошибка ввода', reply_markup=user_markup)
        bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)





bot.polling(none_stop=True, interval = 0)





