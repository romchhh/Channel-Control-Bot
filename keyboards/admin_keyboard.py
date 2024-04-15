from telebot.types import *

def admin():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[KeyboardButton(name) for name in ['👥 Статистика', '📩 Рассылка']])
    #keyboard.add(*[KeyboardButton(name) for name in ['🗂 Вигрузить БД']])
    return keyboard
