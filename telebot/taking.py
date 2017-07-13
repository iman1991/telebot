import telebot
import handlers
import settings
import inDB

bot = telebot.TeleBot(settings.token)

text_id = settings.text_id

back_menu_list = settings.back_menu_list

main_menu_list = settings.main_menu_list

def get_score(message):
    uid = message.from_user.id
    res = inDB.score(uid)
    return res

def check(message):
    uid = message.from_user.id
    res = inDB.score(uid)
    user_markup = telebot.types.ReplyKeyboardMarkup()
    if message.text.isdigit():
        # global infuser
        # infuser['param']['idv'] = int(message.text)
        # infuser['param']['idT'] = message.from_user.id
        # infuser['param']['score'] = res
        bot.send_message(message.from_user.id, '1 литр 4₽\nПоднесите тару к водомату и нажмите кноку "Старт" на аппарате.', reply_markup=user_markup)
        # j = json.dumps(infuser)
        # sock.send(j.encode("utf-8"))
        # data = sock.recv(2048)
    elif message.text != "Назад":
        handlers.answer_text(message, 'Ошибка ввода', handlers.generator_menu(message, back_menu_list))
        sent = handlers.answer_text(message, text_id, handlers.generator_menu(message, back_menu_list))
        bot.register_next_step_handler(sent, check)
