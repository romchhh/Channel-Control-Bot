import logging
from aiogram import Bot, Dispatcher, executor, types

# Токен бота
TOKEN = '7056521734:AAFqcSTLSWgsEec_GVnhDtifqSTAuRft0Ic'

# Ініціалізація бота та диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Вмикаємо логування
logging.basicConfig(level=logging.INFO)

# Хендлер на заявку на вступ до каналу
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS, is_chat_admin=True)
async def new_member_request(message: types.Message):
    # Отримуємо інформацію про нового учасника
    new_member = message.new_chat_members[0]

    # Формуємо привітальне повідомлення
    welcome_message = f'Привіт, {new_member.first_name}! \nМи раді тобі у нашому каналі!'

    # Відправляємо привітальне повідомлення новому учаснику в особистий чат
    await bot.send_message(chat_id=new_member.id, text=welcome_message)

    # Видаляємо нового учасника з каналу
    await bot.kick_chat_member(chat_id=message.chat.id, user_id=new_member.id)

# Запускаємо бота
if __name__ == '__main__':
    executor.start_polling(dp)
