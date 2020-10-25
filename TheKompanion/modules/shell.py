# by my Kawaii neko t.me/TheKneesocks >////////////////////<
import html
import asyncio
from telethon import events
from TheKompanion import Kompanion

@Kompanion.on(events.NewMessage(outgoing=True, pattern=r'\.(?:shell|sh|bash|term) (.+)(?:\n([\s\S]+))?'))
async def run_shell(e):
    cmd, stdin = e.pattern_match.group(1), e.pattern_match.group(2)
    stdin = stdin.encode() if stdin else None
    ptext = 'Type[sh]\n'
    ptext += f'<code>{html.escape(cmd)}</code>\n'
    if stdin:
        ptext += 'stdin \\\n'
        ptext += f'<code>{html.escape(stdin.decode())}</code>\n\n'
    text = ptext
    text += 'RC[undefined]'
    await e.edit(text, parse_mode='html')
    proc = await asyncio.create_subprocess_exec(
        'bash', '-c', '--', cmd, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate(stdin)
    text = ptext
    text += f'RC[{proc.returncode}]\n'
    text += f'stderr \\\n<code>{html.escape(stderr.decode())}</code>\n\n' if stderr else ''
    text += f'stdout \\\n<code>{html.escape(stdout.decode())}</code>' if stdout else ''
    await e.edit(text, parse_mode='html')
