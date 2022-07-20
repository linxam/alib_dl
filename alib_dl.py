#!/usr/bin/env python3

import json
import pathlib
import requests
import os
import sys

# получаем веб-страницу с книгой
url = 'https://knigorai.com/books/162320'
# ~ url = sys.argv[-1]
r = requests.get(url)
f = open('tempfile.txt', 'wb')
f.write(r.content)
f.close()

# из полученной веб-страницы, получаем адрес и название плейлиста
f = open('tempfile.txt', 'r')
playlist = ''
for line in f:
	if line.strip().startswith('var player = new'):
		playlist = line.strip()
playlist = playlist[playlist.index('{'):-2]
playlist = playlist.replace('id', '"id"')
playlist = playlist.replace('title', '"title"')
playlist = playlist.replace('file', '"file"')
playlist_obj = json.loads(playlist)
# print(playlist_obj)

# получаем сам плейлист
r = requests.get(playlist_obj['file'])
f = open(playlist_obj['title']+'.txt', 'wb')
f.write(r.content)
f.close()

# создаем папку для скачиваемых файлов
if not os.path.exists(playlist_obj['title']):
    os.makedirs(playlist_obj['title'])

# print(pathlib.Path().absolute())

# парсим инфу из плейлиста
datafile = open(playlist_obj['title']+'.txt')
data = json.load(datafile)

# скачиваем файлы в папку книги
for i in data:
	print('Downloading file:', i['title'])
	r = requests.get(i['file'])
	f = open(os.path.join(playlist_obj['title'], i['title']+'.mp3'), 'wb')
	f.write(r.content)
	f.close()

if os.path.exists(playlist_obj['title'] + '.txt'):
	print('removing file:', playlist_obj['title'] + '.txt')
	os.remove(playlist_obj['title'] + '.txt')
if os.path.exists('tempfile.txt'):
	print('removing file:', 'tempfile.txt')
	os.remove('tempfile.txt')

print('done')

