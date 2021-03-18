#!/usr/bin/env python3
from pyrogram import Client
from pyrogram.types import ChatMember

from user_bot_kit import retry
from user_bot_kit.groups import get_super_groups
from user_bot_kit.users import remove_member, get_users

app = Client("bot")


async def clean_deleted_account(chat_id: int):
    remove = retry(remove_member)
    async for member in get_users(app, chat_id):
        member: ChatMember
        if not member.user.is_deleted:
            continue
        await remove(app, chat_id, member)


def main():
    app.start()
    for chat in get_super_groups(app):
        print("#%s (%s)" % (chat.title, chat.id))
        clean_deleted_account(chat.id)
    app.stop()


if __name__ == "__main__":
    main()
