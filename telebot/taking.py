import telebot
import handlers
import settings
import inDB
import json
import socket
import gateway


sock = socket.socket()

sock.connect(('127.0.0.1', 8080))


bot = telebot.TeleBot(settings.token)

text_id = settings.text_id

text_water = settings.text_water

command_error = settings.command_error

back_menu_list = settings.back_menu_list

main_menu_list = settings.main_menu_list

def get_score(message):
    uid = message.from_user.id
    res = inDB.score(uid)
    return res

def check(message):
    if message.text.isdigit():
        param = {
                    'idv':int(message.text),
                    'idT':message.from_user.id,
                    'score':get_score(message)
                }
        gatewey.infuser.update({'param':param})
        j = json.dumps(gateway.infuser)
        sock.send(j.encode("utf-8"))
        sock.shutdown(socket.RDWR)
        sock.close()
        handlers.answer_text(message, text_water, handlers.generator_menu(message, back_menu_list))
    elif message.text != "Назад":
        handlers.answer_text(message, command_error, handlers.generator_menu(message, main_menu_list))