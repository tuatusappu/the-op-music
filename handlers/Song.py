import os
import requests
import aiohttp
import youtube_dl

from pyrogram import filters, Client
from youtube_search import YoutubeSearch

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🌺𝚁𝚄𝙺𝙾 𝚉𝙰𝚁𝙰 𝚂𝙰𝙱𝙰𝚁 𝙺𝙰𝚁𝙾 ⭐ 𝚂𝙾𝙽𝙶 𝙳𝙷𝚄𝙽𝙳𝙷 𝚁𝙰𝙷𝙰 𝙷𝚄 ...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "🌋𝐒𝐎𝐍𝐆 𝐍𝐀𝐇𝐈 𝐌𝐈𝐋𝐀 🥺."
        )
        print(str(e))
        return
    m.edit("𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗦𝗼𝗻𝗴 🌺 𝐅𝐑𝐎𝐌 𝐀𝐁𝐇𝐈 𝐒𝐄𝐑𝐕𝐄𝐑...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '**🎵 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗱 𝗕𝘆 :- ✨@ITZ_R0CKSTAR  ❤️☝️**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('🌸 𝐀𝐁𝐇𝐈 𝗡𝗼𝘁 𝗚𝗶𝘃𝗲 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝗙𝗼𝗿 𝗚𝗶𝘃𝗶𝗻𝗴 𝗬𝗼u 💿 𝗦𝗼𝗻𝗴 𝐅𝐑𝐎𝐌 𝗥𝗢𝗖𝗞𝗦𝗧𝗔𝗥 𝐒𝐄𝐑𝐕𝐄𝐑')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
