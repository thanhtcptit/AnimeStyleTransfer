import os
import re
import json
import codecs


def load_txt(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        data = [line.rstrip('\n') for line in f]
        return data


def load_dict(filename):
    d = {}
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f:
            data = line.strip().split()
            d[data[0]] = data[1]
    return d


def load_csv(filename):
    data = []
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f:
            data.append(line.strip().split(','))
    return data


def save_txt(filename, data):
    with codecs.open(filename, encoding='utf-8', mode='w+') as f:
        for item in data:
            f.write(str(item) + '\n')


def save_json(filename, data):
    with codecs.open(filename, 'w') as f:
        for item in data:
            strs = json.dumps(item)
            f.write(str(strs) + '\n')


def append_json(f, data):
    assert f.mode.startswith("a"), "should only use this function to append"
    for item in data:
        strs = json.dumps(item)
        f.write(str(strs) + '\n')
    if close and not f.closed:
        f.close()


def load_json(filename):
    with codecs.open(filename, 'r') as f:
        return json.load(f)
