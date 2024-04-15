from telebot import types

def get_join_request_keyboard():
    button1 = types.InlineKeyboardButton("Канал 1", url="https://t.me/vchempower")
    #button2 = types.InlineKeyboardButton("Канал 2", url="https://t.me/testyktestyk2")
    #button3 = types.InlineKeyboardButton("Канал 3", url="https://t.me/testyktestyk3")
    #button4 = types.InlineKeyboardButton("Канал 4", url="https://t.me/channel4")
    #button5 = types.InlineKeyboardButton("Канал 5", url="https://t.me/channel5")
    #button6 = types.InlineKeyboardButton("Канал 5", url="https://t.me/channel5")
    button7 = types.InlineKeyboardButton("Проверить подписку ✅", callback_data="check_subscriptions")

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button1, button7)

    return keyboard

