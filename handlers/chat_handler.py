import logging

from aiogram import types
from executor import bot, dp
from middlewares.json_togo import read_json, write_json
from middlewares.chats import add_new_chat
from datetime import timedelta


def read_data():
    return read_json('./data.json')


restricted_date = read_data()['banhammer_date']


@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def say_hello(message: types.Message):
    await bot.send_message(message.from_user.id, "Hey Whatsup!\n"
                                                 "Для начала работы добавьте меня в группу и "
                                                 "сделайте ее администратором\n\n"
                                                 "Для обьявления даты начала блокировки отправьте мне команду:\n\n"
                                                 "/banfromdate YYYY-MM-DD\n\n"
                                                 "Для отключения блокировки удалите меня из группы "
                                                 "или лишите прав администратора")


@dp.message_handler(commands=["exit"], chat_type=types.ChatType.PRIVATE)
async def goodbye(message: types.Message):
    rmv_kb = types.ReplyKeyboardRemove()
    await message.reply('Всего доброго!', reply_markup=rmv_kb)


@dp.message_handler(text=['Выход'], chat_type=types.ChatType.PRIVATE)
async def ext(message: types.Message):
    rmv_kb = types.ReplyKeyboardRemove()
    await message.reply('Всего доброго!', reply_markup=rmv_kb)


@dp.message_handler(commands=['banfromdate'], chat_type=types.ChatType.PRIVATE)
async def ext(message: types.Message):
    date = message.text.split(" ")[1] + " 00:00:00"
    data = read_data()
    data["banhammer_date"] = date
    write_json("./data.json", data)


@dp.message_handler(lambda message:
                    (str(message.date) > restricted_date) and
                    ('group' in message.chat.type))
async def banhammer(message: types.Message):
    data = read_data()
    if str(message.chat.id) not in list(data["chats"].keys()):
        await add_new_chat(message, datafile=data)
    else:
        admin_chat_id = data["chats"][str(message.chat.id)]["admins"]
        if message.from_user.id not in admin_chat_id:
            try:
                await bot.ban_chat_member(message.chat.id, message.from_user.id, timedelta(seconds=45))
                data["chats"][str(message.chat.id)]["banned_users"].append(message.from_user.id)
                write_json('./data.json', data)
            except Exception as e:
                logging.error(e)
