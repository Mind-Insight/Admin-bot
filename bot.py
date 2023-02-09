from aiogram import Dispatcher, types, executor, Bot
from config import TOKEN, CHANNEL_ID, CHANNEL_URL, GROUP_ID, ADMIN_ID, FORBIDDEN_WORDS
import logging
from keyboards import kb
from database import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database("db.db")


def check_subscription(user):
    return user['status'] != 'left'


@dp.message_handler(commands=['mute'])
async def mute(message: types.Message):
    if str(message.from_user.id) == ADMIN_ID:
        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение")
            return
        mute_seconds = int(message.text[6:])
        db.add_mute(message.reply_to_message.from_user.id, mute_seconds)
        await message.reply_to_message.reply(f"Пользователь был замучен на {mute_seconds} секунд")


@dp.message_handler(content_types=['new_chat_members'])
async def greet(message: types.Message):
    await message.answer("Добро пожаловать\nПодпишитесь на канал, чтобы отправлять сообщения", reply_markup=kb)


@dp.message_handler()
async def message(message: types.Message):
    if not db.exists(message.from_user.id):
        db.add_user(message.from_user.id)

    if not db.mute(message.from_user.id):
        if check_subscription(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
            text = message.text.lower()
            for word in FORBIDDEN_WORDS:
                if word in text:
                    await message.delete()

        else:
            await message.answer("Вы не подписаны на канал!", reply_markup=kb)
            await message.delete()
    else:
        await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
