# -*- coding: utf-8 -*-
import datetime
import os
import time
from typing import Dict, List, Any, Union

import discord
from discord import FFmpegPCMAudio, Embed, Colour
from discord.utils import get
from dotenv import load_dotenv
from youtube_dl import YoutubeDL

import PyPaperBot.__main__ as pb
from bot_package import tiktaktoe, fetcher, mmr, yt

# Load PW from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# CONSTANTS
PREFIX = '!'
NEXTLINE = '\n'

PLAYER: Dict[str, Union[List[Any], None, bool, int, Embed, str]] = {
    'playlist': [],
    'nextone': None,
    'curr': None,
    'tempe': None,
    'loop': False,
    'counter': 0,
    'timer': time.time()
}

players = {}
client = discord.Client()
description = '''A bot for playing music from Spotify.'''


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'{member.name}, welcome to this Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == PREFIX:
        command = str(message.content).split(' ')[0]

        if "connect" in command:
            vc = message.author.voice.channel
            await vc.connect()

        if "cmd" in command:
            return await message.channel.send(
                """```
            !play <link> or <song name> : play song or search song to play
            !take <1-5>                 : choose a song from search result
            !dl <link>                  : download song
            !loop                       : loop song on/off
            !info                       : song info
            !skip                       : skip to next song
            
            !get_paper <DOI>            : download the Paper
            !get_bibtex <DOI>           : download the reference in bibtex format
            
            !TTT                        : play TikTakToe
            !<1-9>                      : choose field
            ```""")

        if "play" in command:
            request = '_'.join(str(message.content).split(' ')[1:])
            if "https://" in request:
                voice = get(client.voice_clients, guild=message.guild)
                if voice is None:
                    vc = message.author.voice.channel
                    await vc.connect()
                voice = get(client.voice_clients, guild=message.guild)
                emb = play(request, voice, message.author.name)
                if emb is None:
                    return await message.channel.send("Queues up")
                return await message.channel.send(embed=emb)
            else:
                PLAYER['tempe'] = fetcher.search_term(request)
                emb = choose_song_message(request, PLAYER['tempe'])
                return await message.channel.send(embed=emb)

        if "info" in command:
            emb: Embed = PLAYER['curr']
            emb.set_field_at(2, name="Playlist: ", value=str(len(PLAYER['playlist'])), inline=True)
            emb.set_field_at(1, name="time playing",
                             value=str(datetime.timedelta(seconds=(time.time() - PLAYER['timer']).__round__())),
                             inline=True)

            return await message.channel.send(embed=PLAYER['curr'])

        if "debug" in command:
            response = "latency: " + str(
                str(PLAYER['counter']) + " " + str(len(PLAYER['playlist'])) + str(
                    get(client.voice_clients, guild=message.guild).latency))
            return await message.channel.send(response)

        if "dl" in command:
            start_time = time.time()
            request = '_'.join(str(message.content).split(' ')[1:])
            yt.get(request)
            for x in os.listdir(r'./music'):
                await message.channel.send(file=discord.File('./music/' + x))
                await message.channel.send("proccessing time: " + str(time.time() - start_time))
                os.remove('./music/' + x)
            return

        if "take" in command:
            request = int(str(message.content).split(' ')[1])
            voice = get(client.voice_clients, guild=message.guild)
            if voice is None:
                vc = message.author.voice.channel
                await vc.connect()
            voice = get(client.voice_clients, guild=message.guild)
            r = play(fetcher.search(PLAYER['tempe'][int(request) - 1]), voice, message.author.name)
            if r is None:
                return await message.channel.send("Queues up")
            return await message.channel.send(embed=PLAYER['curr'])

        if "MMR" in command:
            # if !MMR:
            mmr.mmr(str(message.content).split(':')[1])
            await message.channel.send(file=discord.File('temp/image.png'))

        if "skip" in command:
            voice = get(client.voice_clients, guild=message.guild)
            voice.stop()

        if "loop" in command:
            PLAYER['loop'] = not PLAYER['loop']
            await message.channel.send("Looping ON: " + str(PLAYER['loop']))

        if "get_bibtex" in command:
            doi = str(message.content).split(' ')[1]
            pb.start(DOIs=doi, restrict=0)
            await message.channel.send(file=discord.File('./Paper/bibtex.bib'))
            with open('./Paper/bibtex.bib', 'r') as file:
                data = file.read()
            await message.channel.send(data)
            return

        if "get_paper" in command:
            doi = str(message.content).split(' ')[1]
            pb.start(DOIs=doi, restrict=1)
            for x in os.listdir("./Paper/"):
                if 'pdf' in x:
                    await message.channel.send(file=discord.File("./Paper/" + x))
                    os.remove("./Paper/" + x)
            return

        if 'TTT' in command:
            response = 'Lets Play a round, rules are simple every number on your numpad represents a field !'
            tiktaktoe.IndexDict["board"] = "........."
            await message.channel.send(response)

        if message.content[1] in '123456789':
            temp = list(tiktaktoe.IndexDict["board"]).copy()

            temp[tiktaktoe.IndexDict[int(message.content[1])]] = 'x'
            tiktaktoe.IndexDict['board'] = ''.join(temp)
            response = tiktaktoe.ttt()

            response = message.author.name + '  ,' + response.strip('@') + tiktaktoe.string_to_board(
                tiktaktoe.IndexDict["board"])
            embed = Embed(colour=Colour(0x53292a))
            embed.set_thumbnail(
                url="https://www.squadhelp.com/story_images/visual_images/12593916.jpg"
            )
            embed.set_footer(
                text=response
            )
            return await message.channel.send(embed=embed)


def play(message, voice, author):
    if not voice.is_playing():
        with YoutubeDL(yt.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(message, download=False)
            url = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(url, **yt.FFMPEG_OPTIONS, executable="driver/ffmpeg/bin/ffmpeg.exe"),
                   after=lambda e: playnext(voice, author))
        PLAYER['timer'] = time.time()
        voice.is_playing()
        embed = song_info_message(author, info['title'], info['thumbnails'][0]['url'], url,
                                  info['duration'], info['uploader'])
        PLAYER['curr'] = embed

        return embed
    else:
        PLAYER['playlist'].append(message)
        return None


def playnext(voice, author):
    if not PLAYER['loop']:
        if PLAYER['playlist']:
            PLAYER['nextone'] = PLAYER['playlist'].pop()
        else:
            return None

    else:
        if PLAYER['counter'] >= len(PLAYER['playlist']):
            PLAYER['counter'] = 0
        PLAYER['nextone'] = PLAYER['playlist'][PLAYER['counter']]
        PLAYER['counter'] += 1

    if not voice.is_playing():
        with YoutubeDL(yt.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(PLAYER['nextone'], download=False)
            url = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(url, **yt.FFMPEG_OPTIONS, executable="driver/ffmpeg/bin/ffmpeg.exe"),
                   after=lambda e: playnext(voice, author))
        PLAYER['timer'] = time.time()
        voice.is_playing()
        embed = song_info_message(author, info['title'], info['thumbnails'][0]['url'], url,
                                  info['duration'], info['uploader'])
        PLAYER['curr'] = embed

        return embed
    else:
        PLAYER['playlist'].append(PLAYER['nextone'])
        return None


# Message Utility
def song_info_message(author, title, icon, url, length, maker):
    embed = discord.Embed(title=title, url=url, description=maker, color=0x8640b5)
    embed.set_author(
        name=author,
        icon_url="https://banner2.cleanpng.com/20180604/sgx/kisspng-omega-sa-symbol-alpha-and-omega-fortnite-omega-5b14d6630852a4.6777973915280922590341.jpg"
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Length  (s)", value=str(datetime.timedelta(seconds=length)), inline=True)
    embed.add_field(name="time playing",
                    value=str(datetime.timedelta(seconds=(time.time() - PLAYER['timer']).__round__())), inline=True)
    embed.add_field(name="Playlist: ", value=str(len(PLAYER['playlist'])), inline=True)
    embed.set_footer(text="Youtube Music ♫")

    return embed


def choose_song_message(title, res):
    embed = discord.Embed(title="Search", description=title, color=0x8220b5)
    if len(res) >= 1:
        embed.add_field(value=res[0], name="1", inline=False)
    if len(res) >= 2:
        embed.add_field(value=res[1], name="2", inline=False)
    if len(res) >= 3:
        embed.add_field(value=res[2], name="3", inline=False)
    if len(res) >= 4:
        embed.add_field(value=res[3], name="4", inline=False)
    if len(res) >= 5:
        embed.add_field(value=res[4], name="5", inline=False)
    embed.set_footer(text="Choose with !take <number>")

    return embed


if __name__ == '__main__':
    client.run(TOKEN)
