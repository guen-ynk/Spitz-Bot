'''
@AUTHOR Guen Yanik
2020
PYTHON JAR API
LICENSE MIT
'''

from subprocess import *

NEXTLINE = '\n'


def jarwrapper(*args):
    process = Popen(['java', '-jar'] + list(args), stdout=PIPE, stderr=PIPE)
    ret = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith(str.encode(NEXTLINE)):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split(str.encode(NEXTLINE))
    if stderr != '':
        ret += stderr.split(str.encode(NEXTLINE))
    ret.remove(str.encode(''))
    return ret


def read_txt(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines
