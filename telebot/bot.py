#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import config
import socket
import json
import pymysql.cursors


def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


bot = telebot.TeleBot(config.token)


def add_user(uid, uname):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT idT FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    if results is None or str(results['idT']) != str(uid):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (idT, name, score) values ( %i, '%s', %i)" % (uid, uname, 0))
        connection.commit()   
        cursor.close()
        return True

def score(uid):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT score FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    res = "{}₽".format(str(results["score"]))
    return res


@bot.message_handler(content_types=['text'])
def prot(message):
    if message.text == 'Назад':
        back(message)
    elif message.text == 'Получить воду':
        get_water(message)
    elif message.text == 'Пополнить баланс':
        add_score(message)
    elif message.text == 'Баланс':
        get_score(message)
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup()
        user_markup.row('Назад')
        bot.send_message(message.from_user.id, 'Команда не найдена', reply_markup=user_markup)


@bot.message_handler(commands=['start'])
def handle_start(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    add_user(uid, uname)
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Получить воду')
    user_markup.row('Пополнить баланс')
    # user_markup.row('Статистика')
    user_markup.row('Баланс')
    bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)


def back(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Получить воду')
    user_markup.row('Пополнить баланс')
    # user_markup.row('Статистика')
    user_markup.row('Баланс')
    bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)



def get_water(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    sent = bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)
    bot.register_next_step_handler(sent, check)


def add_score(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)


# @bot.message_handler(regexp='Статистика')
# def handle_start(message):
#     user_markup = telebot.types.ReplyKeyboardMarkup()
#     user_markup.row('Назад')
#     bot.send_message(message.from_user.id, 'OK', reply_markup=user_markup)


def get_score(message):
    uid = message.from_user.id
    res = score(uid)
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    bot.send_message(message.from_user.id, res, reply_markup=user_markup)



def check(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    if message.text.isdigit():
        bot.send_message(message.from_user.id, '1 литр 4₽\nПоднесите тару к водомату и нажмите кноку "Старт" на аппарате.', reply_markup=user_markup)
    elif not (message.text.isdigit()) and not "Назад":
        bot.send_message(message.from_user.id, 'Ошибка ввода', reply_markup=user_markup)
        bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)



bot.polling(none_stop=True, interval = 0)
