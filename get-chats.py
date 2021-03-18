#!/usr/bin/env python3
from pyrogram import Client
from pyrogram.types import Chat, Dialog

app = Client("bot")


async def get_chats():
    self_id = (await app.get_me()).id
    async for dialog in app.iter_dialogs():
        dialog: Dialog
        chat = dialog.chat
        status = None
        try:
            status = (await chat.get_member(self_id)).status
        except:
            pass
        yield chat, status


def display_name(chat: Chat):
    if chat.title:
        return chat.title
    if chat.last_name:
        return chat.first_name + " " + chat.last_name
    return chat.first_name


async def main():
    await app.start()
    async for chat, status in get_chats():
        row = "#%14s | %-20s | %-40s | %-13s | %s" % (
            chat.type,
            chat.id,
            chat.username or "",
            status or "",
            display_name(chat),
        )
        print(row)
    await app.stop()


if __name__ == "__main__":
    main()
