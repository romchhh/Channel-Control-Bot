import telebot
from keyboards.user_keyboard import get_join_request_keyboard
from config import bot_token, admins, enter_channel, channel1
import db
from keyboards.admin_keyboard import admin
from telebot import types
import io
import openpyxl
import io

bot = telebot.TeleBot(bot_token)

@bot.chat_join_request_handler()
def handle_join_request(message):
    user_id = message.from_user.id
    first_name  = message.from_user.first_name
    user_data = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    db.init_db()
    db.save_user_data(user_id, user_data)

    keyboard = get_join_request_keyboard()
    bot.send_message(user_id, f"<b>Добрый день, {first_name}!</b> Прежде чем получить доступ к основной базе знаний ,\n подпишись на остальные каналы. \n<i>Благодарю за понимание и интерес к моему контенту!</i>", parse_mode='HTML', reply_markup=keyboard)

import re

@bot.callback_query_handler(func=lambda call: call.data == "check_subscriptions")
def check_subscriptions(call):
    user_id = call.from_user.id
    chat_name = '@vchempower'

    try:
        chat = bot.get_chat(chat_name)
        member = bot.get_chat_member(chat.id, user_id)

        if member.status in ["member", "creator", "administrator"]:
            bot.answer_callback_query(call.id, "Вы подписаны на канал!")
            bot.approve_chat_join_request(enter_channel, user_id)
        else:
            bot.answer_callback_query(call.id, "Вы не подписаны на канал. Пожалуйста, подпишитесь на канал и проверьте подписку еще раз.")
    except Exception as e:
        print(f"Error checking subscription for chat {chat_name}: {e}")
        bot.answer_callback_query(call.id, "Произошла ошибка при проверке подписки. Пожалуйста, попробуйте еще раз.")



@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if user_id in admins:
        bot.send_message(user_id, "👨🏼‍💻 Админ панель:", reply_markup=admin())



@bot.message_handler(func=lambda message: message.text == '🗂 Вигрузить БД' and message.from_user.id in admins)
def get_DB(message):
    user_data = db.get_all_user_data()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "UserData"

    headers = ['id', 'username', 'first_name', 'last_name']
    ws.append(headers)

    for row in user_data:
        ws.append([row['id'], row['username'], row['first_name'], row['last_name']])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    bot.send_document(chat_id=message.chat.id, document=output, filename='UserData.xlsx')



    
    
@bot.message_handler(func=lambda message: message.text == '📩 Рассылка' and message.from_user.id in admins)
def send_broadcast_prompt(message):

    bot.send_message(message.chat.id, 'Текст рассылки поддерживает разметку *HTML*, то есть:\n'
                                      '<b>*Жирный*</b>\n'
                                      '<i>_Курсив_</i>\n'
                                      '<pre>`Моноширный`</pre>\n'
                                      '<a href="ссылка-на-сайт">[Обернуть текст в ссылку](test.ru)</a>'.format(),
                             parse_mode="markdown")
    bot.send_message(message.chat.id, "Введите текст сообщения или нажмите /skip, чтобы пропустить:")
    bot.register_next_step_handler(message, process_broadcast_text)
def process_broadcast_text(message):
    bot.process_broadcast_text = message.text
    
    bot.send_message(message.chat.id, "Отправьте фото для добавления к сообщению или нажмите /skip, чтобы пропустить:")
    bot.register_next_step_handler(message, process_broadcast_photo)

def process_broadcast_photo(message):
    if message.text == '/skip':
        send_preview(message.chat.id)
    elif message.photo:
        bot.process_broadcast_photo = message.photo[0].file_id
        send_preview(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте фото или нажмите /skip, чтобы пропустить.")

def send_preview(chat_id):
    markup = types.InlineKeyboardMarkup()
    preview_button = types.InlineKeyboardButton("📤 Отправить", callback_data="send_broadcast")
    cancel_button = types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_broadcast")
    markup.row(preview_button, cancel_button)
    markup.one_time_keyboard = True
    
    text = "📣 *Предварительный просмотр рассылки:*\n\n"
    text += bot.process_broadcast_text 
    
    if hasattr(bot, "process_broadcast_photo"):
        bot.send_photo(chat_id, bot.process_broadcast_photo, caption=text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "send_broadcast")
def send_broadcast_to_users_callback(call):
    text = bot.process_broadcast_text
    photo = bot.process_broadcast_photo if hasattr(bot, "process_broadcast_photo") else None
    send_broadcast_to_users(text, photo, call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_broadcast")
def cancel_broadcast_callback(call):
    bot.send_message(call.message.chat.id, "Рассылка отменена.")
    del bot.process_broadcast_text
    if hasattr(bot, "process_broadcast_photo"):
        del bot.process_broadcast_photo
    admin(call.message) 

def send_broadcast_to_users(text, photo, chat_id):
    try:
        user_ids = db.get_all_user_ids() 
        for user_id in user_ids:
            try:
                if photo:
                    bot.send_photo(user_id, photo, caption=text, parse_mode='HTML')
                else:
                    bot.send_message(user_id, text, parse_mode='HTML')
            except Exception as e:
                print(f"Error sending message to user with ID {user_id}: {str(e)}")
        
        bot.send_message(chat_id, f"Рассылка успешно выполнена для {len(user_ids)} пользователей.")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")
        
        
        
@bot.message_handler(func=lambda message: message.text == '👥 Статистика' and message.from_user.id in admins)
def send_user_statistics(message):
    try:
        total_users = db.get_total_users()
        text = "👥 *Количество пользователей в базе данных:* {0}\n".format(total_users)

        bot.send_message(message.chat.id, text, parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
            
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print (e)
            

