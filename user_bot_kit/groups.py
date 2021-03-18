from pyrogram import Client
from pyrogram.types import Dialog


async def get_super_groups(app: Client):
    self_id = (await app.get_me()).id
    async for dialog in app.iter_dialogs():
        dialog: Dialog
        chat = dialog.chat
        if chat.type != "supergroup":
            continue
        try:
            member = await app.get_chat_member(chat.id, self_id)
            if not member.can_restrict_members:
                continue
        except Exception as e:
            print("#%s (%s): %s" % (chat.title, chat.id, repr(e)))
            continue
        yield chat
