import os

import youtube_dl

path = os.path.dirname(__file__)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './music/%(title)s.%(ext)s',
    'ffmpeg_location': 'driver/ffmpeg/bin/',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': 'True'
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


def get(link):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(ydl_opts["outtmpl"])
        ydl.download([link])
        return ("./music")
