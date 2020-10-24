from time import time_ns
from TheKompanion.helpers import command
from TheKompanion import Kompanion

@Kompanion.on(command(pattern = "ping"))
async def ping(event):
    start = time_ns()
    await event.edit("`Ping…`")
    time_taken_ms = int((time_ns() - start) / 1000000)
    await event.edit(f"`Pong!\n `**{time_taken_ms}**`ms`")