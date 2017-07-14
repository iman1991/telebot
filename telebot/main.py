#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import settings
import inDB
import handlers
import taking
import socket
import json
import gateway

infuser = gateway.infuser

bot = telebot.TeleBot(settings.token)

text_welcome = settings.text_welcome

text_get = settings.text_get

text_id = settings.text_id

text_error = settings.text_error

back_menu_list = settings.back_menu_list

main_menu_list = settings.main_menu_list



@bot.message_handler(commands=['start'])
def handle_start(message):
    inDB.add_user(message.from_user.id, message.chat.first_name)
    handlers.answer_text(message, text_welcome, handlers.generator_menu(message, main_menu_list))


@bot.message_handler(regexp='Получить воду')
def handle_start(message):
    infuser.update({'methed':'GetWater'})
    sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
    bot.register_next_step_handler(sent, taking.check)


@bot.message_handler(regexp='Пополнить баланс')
def handle_start(message):
    sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
    bot.register_next_step_handler(sent, taking.check)


@bot.message_handler(regexp='Баланс')
def handle_start(message):
    handlers.answer_text(message, "{}₽".format(taking.get_score(message)), handlers.generator_menu(message, back_menu_list))


@bot.message_handler(regexp='Назад')
def handle_start(message):
    handlers.answer_text(message, text_get, handlers.generator_menu(message, main_menu_list))




bot.polling(none_stop=True, interval = 0)




