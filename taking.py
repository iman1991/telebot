import telebot
import handlers
from settings import *
import inDB
import json
import socket
import gateway
import connection


bot = telebot.TeleBot(token)


sock = connection.connect_shluz()

def get_score(message):
    uid = message.from_user.id
    res = inDB.score(uid)
    return res

def balance(message):
    if 0 >= get_score(message):
        return False
    else:
        return True

def get_vodomat(message):
    if message.text.isdigit():
        vid = int(message.text)
        res = inDB.vodomat(vid)
    else:
        res = False
    return res

def check(message):
    if balance(message):
        if get_vodomat(message):
            if message.text.isdigit():
                sock = connection.connect_shluz()
                param = {
                            'idv': int(message.text),
                            'idT': message.from_user.id,
                            'score': get_score(message)
                }
                gateway.infuser.update({'param':param})
                j = json.dumps(gateway.infuser)
                sock.send(j.encode("utf-8"))
                inDB.add_id(message.from_user.id, int(message.text))
                handlers.answer_text(message, text_water, handlers.generator_menu(message, stop_menu_list))
            elif message.text != "Остановить":
                handlers.answer_text(message, command_error, handlers.generator_menu(message, main_menu_list))
        elif message.text != "Назад":
            handlers.answer_text(message, command_error, handlers.generator_menu(message, main_menu_list))
    else:
        handlers.answer_text(message, balance_empty, handlers.generator_menu(message, main_menu_list))









