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
import connection


bot = telebot.TeleBot(settings.token)

text_welcome = settings.text_welcome

balance_empty = settings.balance_empty

text_get = settings.text_get

text_id = settings.text_id

text_error = settings.text_error

back_menu_list = settings.back_menu_list

main_menu_list = settings.main_menu_list



@bot.message_handler(commands=['start'])
def handle_start(message):
    inDB.add_user(message.from_user.id, message.chat.first_name)
    handlers.answer_text(message, text_welcome, handlers.generator_menu(message, main_menu_list))


@bot.message_handler(regexp='Активировать')
def handle_start(message):
    gateway.infuser.update({'method':'Activate'})
    if taking.balance(message):
        sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
        bot.register_next_step_handler(sent, taking.check)
    else:
        handlers.answer_text(message, balance_empty, handlers.generator_menu(message, main_menu_list))


@bot.message_handler(regexp='Баланс')
def handle_start(message):
    handlers.answer_text(message, "{}₽".format(taking.get_score(message)), handlers.generator_menu(message, main_menu_list))


@bot.message_handler(regexp='Назад')
def handle_start(message):
    handlers.answer_text(message, text_get, handlers.generator_menu(message, main_menu_list))


@bot.message_handler(regexp='Остановить')
def handle_start(message):
    gateway.infuser.update({'method':'Stop'})
    sock = connection.connect_shluz()
    param = {
                'idv': int(inDB.get_id_v(message.from_user.id)),
                'idT': inDB.get_id(message.from_user.id),
                'score': taking.get_score(message)
    }
    gateway.infuser.update({'param':param})
    j = json.dumps(gateway.infuser)
    sock.send(j.encode("utf-8"))
    #sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    handlers.answer_text(message, text_get, handlers.generator_menu(message, main_menu_list))




bot.polling(none_stop=True, interval = 0)




