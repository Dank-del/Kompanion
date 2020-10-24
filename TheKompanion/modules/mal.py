# by my kawaii neko -> t.me/TheKneeSocks
import asyncio
import html
from jikanpy import AioJikan
from telethon import events
from TheKompanion import Kompanion


zws = '\u200b'

@Kompanion.on(events.NewMessage(outgoing=True, pattern=r'\.my?a(?:nime)?l(?:ist)? a(?:nime)? (.+)'))
async def mal_anime(e):
    await e.edit('Searching...')
    await e.delete()
    async with AioJikan() as jikan:
        sr = await jikan.search('anime', e.pattern_match.group(1))
        a = await jikan.anime(sr['results'][0]['mal_id'])
    if not a:
        await e.reply('err \\\nNo results found')
        return
    text = f'<b>{html.escape(a["title"])}'
    if a['title_japanese']:
        text += f' ({html.escape(a["title_japanese"])})'
    text += '</b>\n'
    text += f'<b>Score:</b> {a["score"]}\n'
    text += f'<b>Type:</b> {html.escape(a["type"])}\n'
    text += f'<b>Genres:</b> {", ".join([html.escape(i["name"]) for i in a["genres"]])}\n'
    text += f'<b>Status:</b> {html.escape(a["status"])}\n'
    text += f'<b>Episodes:</b> {a["episodes"]}\n'
    text += f'<b>Duration:</b> {html.escape(a["duration"])}\n'
    text += f'<i>{html.escape(a["synopsis"])}</i>\n'
    pic = f'{a["image_url"]}'
    url = f'<a href="{html.escape(a["url"])}">read more</a>'
    text = text.strip()
    if len(text) > 1024:
        text =text[0:500] + ".... "
    text = text + url
    await e.reply(text, file=pic, link_preview=False, parse_mode='html')

@Kompanion.on(events.NewMessage(outgoing=True, pattern=r'\.my?a(?:nime)?l(?:ist)? m(?:anga)? (.+)'))
async def mal_manga(e):
    await e.edit('Searching...')
    await e.delete()
    async with AioJikan() as jikan:
        sr = await jikan.search('manga', e.pattern_match.group(1))
        m = await jikan.manga(sr['results'][0]['mal_id'])
    if not m:
        await e.reply('err \\\nNo results found')
        return
    text = f'<b>{html.escape(m["title"])}'
    if m['title_japanese']:
        text += f' ({html.escape(m["title_japanese"])})'
    text += '</b>\n'
    text += f'<b>Score:</b> {m["score"]}\n'
    text += f'<b>Type:</b> {html.escape(m["type"])}\n'
    text += f'<b>Genres:</b> {", ".join([html.escape(i["name"]) for i in m["genres"]])}\n'
    text += f'<b>Status:</b> {html.escape(m["status"])}\n'
    if m['volumes']:
        text += f'<b>Volumes:</b> {m["volumes"]}\n'
    if m['chapters']:
        text += f'<b>Chapters:</b> {m["chapters"]}\n'
    text += f'<i>{html.escape(m["synopsis"])}</i>\n'
    pic = f'{m["image_url"]}'
    url = f'<a href="{html.escape(m["url"])}">read more</a>'
    text = text.strip()
    if len(text) > 1024:
        text =text[0:500] + ".... "
    text = text + url
    await e.reply(text, file=pic, link_preview=False, parse_mode='html')

@Kompanion.on(events.NewMessage(outgoing=True, pattern=r'\.my?a(?:nime)?l(?:ist)? c(?:haracter)? (.+)'))
async def mal_character(e):
    await e.edit('Searching...')
    await e.delete()
    async with AioJikan() as jikan:
        sr = await jikan.search('character', e.pattern_match.group(1))
        c = await jikan.character(sr['results'][0]['mal_id'])
    if not c:
        await e.reply('err \\\nNo results found')
        return
    text = f'<b>{html.escape(c["name"])}'
    if c['name_kanji']:
        text += f' ({html.escape(c["name_kanji"])})'
    text += '</b>\n'
    about = html.escape(c['about'].replace('\\n', ''))
    text += f'<i>{about}</i>\n'
    pic = f'{c["image_url"]}'
    url = f'<a href="{html.escape(c["url"])}">read more</a>'
    text = text.strip()
    if len(text) > 1024:
        text =text[0:500] + ".... "
    text = text + url
    await e.reply(text, file=pic, link_preview=False, parse_mode='html')
    
    
@Kompanion.on(events.NewMessage(outgoing=True, pattern="^.weebhelp"))   
async def help(event):
    msg = """
        **Kompanion. Weeb mod**
        `.myanimelist anime <<anime name>>` -> search anime.
        `.myanimelist character <<character name>>` -> search character.
        `.myanimelist manga <<manga name>>` -> search manga.
    """
    await event.edit(msg)
