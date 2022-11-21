from middlewares.json_togo import write_json


def fetch_admins(admins):
    admin_list = []
    for admin in admins:
        if not admin.user.is_bot:
            admin_list.append(admin.user.id)
    return admin_list


async def add_new_chat(message, datafile):
    admins = await message.chat.get_administrators()
    chat = Chat(message, admins)
    datafile["chats"][message.chat.id] = {
        "title": chat.title,
        "admins": chat.admins,
        "banned_users": chat.banned_users
    }
    write_json('./data.json', datafile)


class Chat:

    def __init__(self, message, admins):
        self.chat_id = message.chat.id,
        self.title = message.chat.title,
        self.admins = fetch_admins(admins)
        self.banned_users = []

