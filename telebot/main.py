#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import settings
import inDB
import handlers
import taking
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
    bot.register_next_step_handler(sent, taking.check)

@bot.message_handler(regexp='Пополнить баланс')
def handle_start(message):
    sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
    bot.register_next_step_handler(sent, taking.check)

@bot.message_handler(regexp='Баланс')
def handle_start(message):
    handlers.answer_text(message, "{}₽".format(get_score(message)), handlers.generator_menu(message, back_menu_list))

@bot.message_handler(regexp='Назад')
def handle_start(message):
    handlers.answer_text(message, text_get, handlers.generator_menu(message, main_menu_list))




def get_score(message):
    uid = message.from_user.id
    res = inDB.score(uid)
    return res





bot.polling(none_stop=True, interval = 0)





