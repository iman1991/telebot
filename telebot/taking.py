import telebot
import handlers
import settings
import inDB
import json
import socket
import gateway



bot = telebot.TeleBot(settings.token)

text_id = settings.text_id

text_get = settings.text_get

text_water = settings.text_water

text_wait = settings.text_wait

command_error = settings.command_error

balance_empty = settings.balance_empty

back_menu_list = settings.back_menu_list

main_menu_list = settings.main_menu_list

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
    vid = int(message.text)
    res = inDB.vodomat(vid)
    return res

def check(message):
    if balance(message):
        if get_vodomat(message):
            if message.text.isdigit():
                sock = socket.socket()
                sock.connect(('127.0.0.1', 9090))
                param = {
                            'idv': int(message.text),
                            'idT': message.from_user.id,
                            'score': get_score(message)
                }
                gateway.infuser.update({'param':param})
                j = json.dumps(gateway.infuser)
                sock.send(j.encode("utf-8"))
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                handlers.answer_text(message, text_water, handlers.generator_menu(message, back_menu_list))
            elif message.text != "Остановить":
                handlers.answer_text(message, command_error, handlers.generator_menu(message, main_menu_list))
        else:
            handlers.answer_text(message, command_error, handlers.generator_menu(message, main_menu_list))
    else:
        handlers.answer_text(message, balance_empty, handlers.generator_menu(message, main_menu_list))









