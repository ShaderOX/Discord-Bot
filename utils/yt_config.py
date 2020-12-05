import discord
import asyncio
import youtube_dl

from time import strftime, gmtime

import os


ytdl_format_options = {
    'format': 'bestaudio/flac',
    'outtmpl': 'songs/%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.song_id = data.get('id')
        self.artist = data.get('uploader')
        thumbnail = data.get('thumbnails')[0]
        self.thumbnail_obj = {
            'url': thumbnail.get('url'),
            'width': thumbnail.get('width'),
            'height': thumbnail.get('height'),
        }
        self.duration_secs = data.get('duration')
        self.filepath = data.get('filepath')
        self.duration = strftime("%M:%S", gmtime(self.duration_secs))
        self.data = data

    @classmethod
    async def from_url(cls, url: str, *, loop=None, stream: bool = False, timestamp: int = 0) -> list:
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        if stream:
            filename = data['url']
        else:
            filename = None
            for f_name in os.listdir("./songs"):
                if data.get('id') in f_name:
                    filename = os.path.join("./songs", f_name)
                    break
            if filename is None:
                filename = ytdl.prepare_filename(data)

        data['filepath'] = filename
        return filename, data


def get_ffmpeg_options(time_start: int = 0) -> dict:
    return {
        'options': f'-vn -ss {time_start}'
    }
