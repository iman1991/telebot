#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import config
import socket
import json
import pymysql


connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='7087',
                             db='vodomat',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def add_user():
    cursor = connection.cursor()
    cursor.execute("SELECT idT FROM users WHERE idT = '%(uid)d'")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if (uid != results):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (idT, name) values ('%(uid)d', '%(uname)d')")
        connection.commit()   
        cursor.close()
        connection.close()
        return True

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="Назад")
def handle_start(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    if (add_user()):
        user_markup = telebot.types.ReplyKeyboardMarkup()
        user_markup.row('Получить воду')
        user_markup.row('Пополнить баланс')
        user_markup.row('Статистика')
        user_markup.row('Баланс')
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
    elif not (message.text.isdigit()):
        bot.send_message(message.from_user.id, 'Ошибка ввода', reply_markup=user_markup)
        bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)



bot.polling(none_stop=True, interval = 0)
