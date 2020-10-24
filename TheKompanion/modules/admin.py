
# Module by t.me/DragSama
from TheKompanion.helpers import command
from TheKompanion import Kompanion

@Kompanion.on(command(pattern = "purge"))
async def purge(event):
    if not event.reply_to_msg_id:
        return
    split = event.text.split(" ", 1)
    if len(split) > 1 and split[1].isnumeric():
        purge_count = int(split[1])
    else:
        purge_count = None
    messages = []
    count = 0
    deleted = False
    async for message in Kompanion.iter_messages(event.chat_id, min_id = event.reply_to_msg_id, reverse = True):
        if purge_count and count == purge_count:
            break
        count += 1
        print(count, purge_count)
        if len(messages) == 100:
            await Kompanion.delete_messages(event.chat_id, messages)
            messages = []
            deleted = True
        else:
            messages.append(message)
            deleted = False
    if len(messages) <= 100:
        if not deleted: # If message were not more than 100 so they never got deleted
            await Kompanion.delete_messages(event.chat_id, messages)
    await Kompanion.send_message(event.chat_id, f"Deleted {count} messages.")



@Kompanion.on(command(pattern=r"(un)?pin", outgoing=True))
async def pin_message(event):
    message_id = event.reply_to_msg_id
    split = event.text.split(" ", 1)
    if len(split) > 1 and split[1] == "loud":
        is_loud = True
    else:
        is_loud = False
    await event.client.pin_message(event.chat_id, message_id, notify = is_loud)
    await event.edit("Message was pinned.")

@Kompanion.on(command(pattern=r"promote", outgoing=True))
async def promote(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit("Reply to someone with .promote to promote them or .promote <username>")
            return
        user = split[1]
    else:
        user = reply.sender_id
    split = event.text.split(" ")
    try:
        if len(split) > 1 and split[1] == "anonymous":
            await Kompanion.edit_admin(event.chat_id, user, is_admin = True, anonymous = True)
            await event.edit("Promoted as anonymous admin!")
        elif len(split) > 1:
            await Kompanion.edit_admin(event.chat_id, user, is_admin = True, title = split[1])
            await event.edit(f"Promoted with custom title {split[1]}!")
        else:
            await Kompanion.edit_admin(event.chat_id, user, is_admin = True, anonymous = False)
            await event.edit("Promoted!")
    except Exception as e:
        await event.edit(str(e))
        return

@Kompanion.on(command(pattern=r"demote", outgoing=True))
async def demote(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit("Reply to someone with .demote to demote them or use .demote <username>")
            return
        user = split[1]
    else:
        user = reply.sender_id
    try:
        await Kompanion.edit_admin(event.chat_id, user, is_admin = False)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.edit("User was demoted")

@Kompanion.on(command(pattern=r"ban", outgoing=True))
async def ban(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit("Reply to someone with .ban to ban them from chat or use .ban <username>")
            return
        user = split[1]
    else:
        user = reply.sender_id
    try:
        await Kompanion.kick_participant(event.chat_id, user)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.edit("User was banned")

@Kompanion.on(command(pattern=r"kick", outgoing=True))
async def kick(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit("Reply to someone with .kick to remove them from chat or use .kick <username>")
            return
        user = split[1]
    else:
        user = reply.sender_id
    try:
        await Kompanion.kick_participant(event.chat_id, user)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.edit("Kicked!")

@Kompanion.on(command(pattern=r"rmdelacc", outgoing=True))
async def deadaccs_finder(event):
    count = 0
    split = event.text.split(" ", 1)
    if len(split) > 1 and split[1] == "kick":
        kick = True
    else:
        kick = False
    msg = await event.reply("Searching participants...")
    async for user in Kompanion.iter_participants(event.chat_id):
        if user.deleted:
            count += 1
            if kick:
                try:
                    await Kompanion.kick_participant(event.chat_id, user)
                except Exception as e:
                    await event.edit("Failed to kick deleted accounts, Make sure you are admin.")
                    print(e)
                    await msg.delete()
                    return
    if not kick:
        await event.edit(f"Found {count} deleted accounts.")
    else:
        await event.edit(f"Kicked {count} deleted accounts.")
    await msg.delete()
    
    

adminhelp = """
    .pin: Pin a message in a group, Do without reply to unpin.\n Format: .pin <loud/None> // As reply (Optional)\n
    .unpin: Unpin a message.\n Format: .unpin\n
    .purge: Purge X messages from replied message.\n Format: .purge <count> // As reply\n
    .promote: Promote a user.\n Format: .promote <username or reply> // As reply (Optional)\n
    .demote: Demotes a user.\n Format: .demote <username or reply> // As reply (Optional)\n
    .ban: Bans a user.\n Format: .ban <username or reply> // As reply (Optional)\n
    .kick: Kick a user.\n Format: .kick <username or reply> // As reply (Optional)\n
    .rmdelacc: Find deleted accounts.\n Format: .rmdelacc <kick>\n
"""


@Kompanion.on(command(pattern = "adminhelp"))
async def helpadmin(event):
    await event.edit(adminhelp)
    
    
    
