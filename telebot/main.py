#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import settings
import handlers
import taking
import socket
import json
import pymysql.cursors


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    answer_text(message, text_welcome, generator_menu(message, main_menu_list))

@bot.message_handler(regexp='Получить воду')
def handle_start(message):
    answer_text(message, text_id, generator_menu(message, back_menu_list))
    # global infuser
    # infuser['method'] = 'GetWater'
    get_water(message)

@bot.message_handler(regexp='Пополнить баланс')
def handle_start(message):
    answer_text(message, text_id, generator_menu(message, back_menu_list))
    add_score(message)

@bot.message_handler(regexp='Баланс')
def handle_start(message):
    answer_text(message, get_score(message), generator_menu(message, back_menu_list))
    get_score(message)

@bot.message_handler(regexp='Назад')
def handle_start(message):
    answer_text(message, text_get, generator_menu(message, main_menu_list))


bot.polling(none_stop=True, interval = 0)





