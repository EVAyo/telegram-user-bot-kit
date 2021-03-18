import time
from datetime import datetime
from typing import List

from pyrogram import Client
from pyrogram.raw.base import UserFull
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.types import ChatMember


async def remove_member(app: Client, chat_id: int, member: ChatMember):
    user_id = member.user.id
    if member.status == "member":
        until_date = int(time.time() + 60)
        await app.kick_chat_member(chat_id, user_id, until_date)
        print("#%s #%s Deleted" % (chat_id, user_id))
    elif member.status in ("kicked", "restricted"):
        await app.unban_chat_member(chat_id, user_id)
        print("#%s #%s Unbanned" % (chat_id, user_id))


async def get_user(app: Client, member: ChatMember, get_bio=False):
    joined_date = None
    if member.joined_date:
        joined_date = datetime \
            .fromtimestamp(member.joined_date) \
            .astimezone() \
            .isoformat()
    bio = None
    if get_bio:
        fully: UserFull = await app.send(GetFullUser(id=await app.resolve_peer(member.user.id)))
        bio = fully.about
    return {
        "User ID": str(member.user.id),
        "Joined Date": joined_date,
        "Status": member.status,
        "Photo": None if member.user.photo else "Unset",
        "First name": member.user.first_name,
        "Last name": member.user.last_name,
        "Username": member.user.username,
        "Bio": bio,
    }


async def get_users(app: Client, chat_id: int, filters: List[str] = None):
    filters = filters or ['kicked', 'restricted', None]
    for filter_name in filters:
        async for member in app.iter_chat_members(chat_id=chat_id, filter=filter_name):
            yield member
