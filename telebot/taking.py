import telebot
import handlers
import settings
import inDB
import json
import socket
import gateway

infuser = gateway.infuser

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
        global infuser
        infuser['param']['idv'] = int(message.text)
        infuser['param']['idT'] = message.from_user.id
        infuser['param']['score'] = get_score(message)
        handlers.answer_text(message, text_water, handlers.generator_menu(message, back_menu_list))
        j = json.dumps(infuser)
        sock.send(j.encode("utf-8"))
        data = sock.recv(2048)
    elif message.text == "Назад":
        pass
    else:
        handlers.answer_text(message, command_error, handlers.generator_menu(message, back_menu_list))
        sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
        bot.register_next_step_handler(sent, check)