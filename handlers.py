import telebot
import settings

bot = telebot.TeleBot(settings.token)

def answer_text(message, answer, user_markup):
    return bot.send_message(message.from_user.id, answer, reply_markup=user_markup)

def generator_menu(message, menu_list):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(item)
    return user_markup