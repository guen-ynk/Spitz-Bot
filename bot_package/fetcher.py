import re
import subprocess
import urllib.request
from subprocess import *

NEXTLINE = '\n'


def search_term(what):
    ret = []
    lol = []
    process = Popen('youtube-dl -e  "ytsearch5:"' + what, stdout=subprocess.PIPE, stderr=PIPE)
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith(str.encode(NEXTLINE)):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split(str.encode(NEXTLINE))
    if stderr != '':
        ret += stderr.split(str.encode(NEXTLINE))
    ret.remove(str.encode(''))
    ret = ret[:-1]
    ret = ret[:5]
    for i in ret:
        lol.append(i.decode('utf-8'))
    return lol


def search(search_key):
    search_keyword = str(search_key).replace(' ', '_')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video = video_ids[:5]
    for i in video:
        i += "https://www.youtube.com/watch?v"
    return video
