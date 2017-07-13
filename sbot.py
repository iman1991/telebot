#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import config
import socket
import json
import pymysql.cursors

bot = telebot.TeleBot(config.token)

infuser={"method":"", "param":{"idT":0, "idv":0, "score":100}}
sock = socket.socket()

sock.connect(('127.0.0.1', 8080))


def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def score(uid):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT score FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    res = results["score"]
    return res
   

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
    res = results["score"]
    return res



text_welcome = "Добро пожаловать!"
text_error = "Команда не найдена ("
back_menu_list = ["Назад"]
main_menu_list = ["Получить воду", "Пополнить баланс", "Баланс"]

def answer_text(message, answer):
    bot.send_message(message.from_user.id, answer)

def generator_menu(message, menu_list):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(menu_list[item])

@bot.message_handler(commands=['start'])
def handle_start(message):
    answer_text(message, text_welcome)
    generator_menu(message, back_menu_list)

@bot.message_handler(regexp='Получить воду')
def handle_start(message):
    generator_menu(message, back_menu_list)
    global infuser
    infuser['method'] = 'GetWater'
    # add_user(uid, uname)
    get_water(message)

@bot.message_handler(regexp='Пополнить баланс')
def handle_start(message):
    generator_menu(message, back_menu_list)

@bot.message_handler(regexp='Баланс')
def handle_start(message):
    generator_menu(message, back_menu_list)

@bot.message_handler(regexp='Назад')
def handle_start(message):
    generator_menu(message, main_menu_list)

@bot.message_handler(content_types=['text'])
def handle_start(message):
    answer_text(message, text_error)


def get_water(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('Назад')
    sent = bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)
    bot.register_next_step_handler(sent, check)



def check(message):
    uid = message.from_user.id
    uname = message.chat.first_name
    res = score(uid)
    user_markup = telebot.types.ReplyKeyboardMarkup()
    if message.text.isdigit():
        global infuser
        infuser['param']['idv'] = int(message.text)
        infuser['param']['idT'] = message.from_user.id
        infuser['param']['score'] = res
        bot.send_message(message.from_user.id, '1 литр 4₽\nПоднесите тару к водомату и нажмите кноку "Старт" на аппарате.', reply_markup=user_markup)
        j = json.dumps(infuser)
        sock.send(j.encode("utf-8"))
        data = sock.recv(2048)
        print(data)
    elif not (message.text.isdigit()) and not "Назад":
        bot.send_message(message.from_user.id, 'Ошибка ввода', reply_markup=user_markup)
        bot.send_message(message.from_user.id, 'Введите ID водомата', reply_markup=user_markup)



bot.polling(none_stop=True, interval = 0)
