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
    connection.close()
    if results is None or str(results['idT']) != str(uid):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (idT, name, score) values ( %i, '%s', %i)" % (uid, uname, 0))
        connection.commit()   
        cursor.close()
        connection.close()
        return True

def score(uid):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT score FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    res = "{}₽".format(str(results["score"]))
    return res

def answer_text(message, answer):
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def prot(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    if message.text == 'Назад':
        add_user(uid, uname)
        back(message)
    elif message.text == 'Получить воду':
        add_user(uid, uname)
        get_water(message)
    elif message.text == 'Пополнить баланс':
        add_user(uid, uname)
        add_score(message)
    elif message.text == 'Баланс':
        add_user(uid, uname)
        get_score(message)
    elif message.text == '/start':
        add_user(uid, uname)
        handle_start(message)
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup()
        user_markup.row('Назад')
        answer_text(message, 'Команда не найдена')


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Получить воду')
    user_markup.row('Пополнить баланс')
    # user_markup.row('Статистика')
    user_markup.row('Баланс')
    answer_text(message, 'Добро пожаловать')


def back(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Получить воду')
    user_markup.row('Пополнить баланс')
    # user_markup.row('Статистика')
    user_markup.row('Баланс')
    answer_text(message, 'Добро пожаловать')


def get_water(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    sent = bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)
    bot.register_next_step_handler(sent, check)


def add_score(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    answer_text(message, 'Введите ID водомата')


# @bot.message_handler(regexp='Статистика')
# def handle_start(message):
#     user_markup = telebot.types.ReplyKeyboardMarkup()
#     user_markup.row('Назад')
#     bot.send_message(message.from_user.id, 'OK', reply_markup=user_markup)


def get_score(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    res = score(uid)
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    answer_text(message, res)



def check(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    if message.text.isdigit():
        answer_text(message, '1 литр 4₽\nПоднесите тару к водомату и нажмите кноку "Старт" на аппарате.')
    elif not (message.text.isdigit()) and not "Назад":
        answer_text(message, 'Ошибка ввода')
        answer_text(message, 'Введите ID водомата')


bot.polling(none_stop=True, interval = 0)