#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import config
import socket
import json
import cherrypy
import config

WEBHOOK_HOST = '194.67.217.180'
WEBHOOK_PORT = 80  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)

# a = {"id":"0","name":"durak"}

# sock = socket.socket()

# sock.connect(("172.18.0.108", 9090))


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="Назад")
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Получить воду', 'Пополнить баланс')
    user_markup.row('Статистика', 'Баланс')
    bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)


@bot.message_handler(regexp='Получить воду')
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    sent = bot.send_message(message.from_user.id, 'На вашем счету XXX рублей...\nВведите ID водомата', reply_markup=user_markup)
    bot.register_next_step_handler(sent, check)



@bot.message_handler(regexp='Пополнить баланс')
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    bot.send_message(message.from_user.id, 'На вашем счету XXX рублей...', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)


@bot.message_handler(regexp='Статистика')
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    bot.send_message(message.from_user.id, 'OK', reply_markup=user_markup)


@bot.message_handler(regexp='Баланс')
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    bot.send_message(message.from_user.id, '150₽', reply_markup=user_markup)



def check(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    if message.text.isdigit():
        bot.send_message(message.from_user.id, '1 литр 4₽\nПоднесите тару к водомату и нажмите кноку "Старт" на аппарате.', reply_markup=user_markup)
        # a['id'] = message.text
        # j = json.dumps(a)
        
        # sock.send(j.encode("utf-8"))
        
        # data = sock.recv(1024)
        # print(data)
    elif not (message.text.isdigit()):
        bot.send_message(message.from_user.id, 'Ошибка ввода', reply_markup=user_markup)
        bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)



bot.polling(none_stop=True, interval = 0)