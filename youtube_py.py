from __future__ import unicode_literals
import os
import requests
import youtube_dl
from googleapiclient.discovery import build

api_youtube = 'AIzaSyDBeZ638MVWKqmi2z8ONN-EvU6Kmrtxwoc'
folder_name = 'musique'


def list_from_txt(txt_file):
    word_list = []
    lines = len(txt_file.readlines())
    txt_file.seek(0)
    for line in range(lines):
        word_list.append(txt_file.readline())
    return word_list



def search_vid(word):
    request = youtube.search().list(q=word, part='snippet', order='viewCount', maxResults=1, type='video')
    response = request.execute()
    searched_vid = "https://www.youtube.com/watch?v=" + response['items'][0]['id']['videoId']
    return searched_vid

def search_playlists(word):
    url_list = []
    request = youtube.search().list(q=word, part='snippet', maxResults=1, type='playlist')
    response = request.execute()
    searched_playl = response['items'][0]['id']['playlistId']
    accept = input("download playlist ? https://www.youtube.com/playlist?list="+searched_playl+" : y or n\n")
    if accept == 'y':
        print("download playlist https://www.youtube.com/playlist?list="+searched_playl)
        request = youtube.playlistItems().list(part='snippet', playlistId=searched_playl, maxResults=20)
        response = request.execute()
        for video in response['items']:
            vid_url = "https://www.youtube.com/watch?v=" + video['snippet']['resourceId']['videoId']
            url_list.append(vid_url)
    else:
        print("download cancelled")
    return url_list

def search_vids_n_playls(word_list):
    urls = []
    for word in word_list:
        if "playlist" in word:
            urls += search_playlists(word[word.find("playlist")+8::])
        else:
            urls.append(search_vid(word))
    return(urls)

def create_folder(folder_name):
    cwd = os.getcwd()
    if not os .path.isdir(cwd+'\\'+ folder_name):
        os.mkdir(cwd+'\\'+ folder_name)
    os.chdir(cwd+'\\'+ folder_name)

txt = open("music_list.txt","r")
word_list = list_from_txt(txt)
youtube = build('youtube', 'v3', developerKey=api_youtube)
urls = search_vids_n_playls(word_list)
for url in urls:
    print("download " + url)
create_folder(folder_name)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download(urls)
    except:pass
