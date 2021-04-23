import re
import string
import subprocess
import urllib.request
from subprocess import *

NEXTLINE = '\n'
printable = string.printable


def search_term(what):
    ret = []
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
    ret = ret[:min(5, len(ret))]
    return list(map(lambda e: e.decode('utf-8'), ret))


def search(search_key):
    search_key= ''.join(filter(lambda x: x in printable, search_key))
    print(search_key)
    search_keyword = str(search_key).replace(' ', '_')
    print(search_keyword)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_id = re.search(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/" + video_id.group(0) if video_id else ""
