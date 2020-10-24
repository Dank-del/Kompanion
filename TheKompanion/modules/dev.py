import asyncio
import inspect
import io
from telethon import events
from TheKompanion import Kompanion
from speedtest import Speedtest
from io import StringIO
import traceback
import sys



@Kompanion.on(events.NewMessage(outgoing=True, pattern="^.speed"))
async def iamspeed(event):
    await event.edit("`Running speed test…`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    await event.edit(
        f"`Started at: {result['timestamp']}\n"
        f"Download: {speed_convert(result['download'])}\n"
        f"Upload: {speed_convert(result['upload'])}\n"
        f"Ping: {result['ping']} milliseconds\n"
        f"ISP: {result['client']['isp']}`"
    )


def speed_convert(size):
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kilobits/s', 2: 'Megabits/s', 3: 'Gigabits/s', 4: 'Terabits/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"



# Thanks to stackoverflow for existing https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
# eval and exec by t.me/DragSama // github.com/DragSama

@Kompanion.on(events.NewMessage(outgoing=True, pattern="^.eval"))
async def evaluate(event):
    split = event.text.split(" ", 1)
    if len(split) == 1:
        await event.edit("Format: .eval <command>")
        return
    try:
        evaluation = eval(split[1])
    except Exception as e:
        evaluation = e
    await event.edit(str(evaluation))


@Kompanion.on(events.NewMessage(outgoing=True, pattern="^.exec"))
async def execute(event):
    split = event.text.split(" ", 1)
    if len(split) == 1:
        await event.edit("Format: .exec <command>")
        return
    stderr, output, wizardry = None, None, None
    code = split[1]
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    try:
        await async_exec(code, event)
    except Exception:
        wizardry = traceback.format_exc()
    output = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    final = f"Command:\n`{code}`\n"
    sys.stderr = old_stderr
    if wizardry:
        final += "**Output**:\n`" + wizardry
    elif output:
        final += "**Output**:\n`" + output
    elif stderr:
        final += "**Output**:\n`" + stderr
    else:
        final = "`OwO no output"
    await event.edit(final + '`')


async def async_exec(code, event):
    exec(
        f'async def __async_exec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__async_exec'](event)



@Kompanion.on(events.NewMessage(outgoing=True, pattern="^.chatid"))
async def chatidgetter(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.forward and reply.forward.channel_id:
            await event.edit(f"**Channel ID:**` {reply.forward.channel_id}`")
            return
        chat_id = reply.chat_id
    else:
        chat_id = event.chat_id

    await event.edit(f"**Chat ID:**` {chat_id}`")
    
@Kompanion.on(events.NewMessage(outgoing=True, pattern="^.devhelp"))   
async def help(event):
    msg = """
        **Kompanion. Dev mod**
        `.eval` -> execute python code.
        `.exec` -> shell.
        `.chatid` -> get chat ID.
        `.chatinfo` -> get chat info. 
        `.speed` -> just a speedtest.
    """
    await event.edit(msg)
    
    
