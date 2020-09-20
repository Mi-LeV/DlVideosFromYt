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
    request = youtube.search().list(q=word, part='snippet', maxResults=1, type='video')
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
        if word:
            if "playlist" in word:
                urls += search_playlists(word[word.find("playlist")+8::])
            else:
                urls.append(search_vid(word))
    return(urls)

def create_folder(folder_name):
    cwd = os.getcwd()
    new_dir = os.path.join(cwd,folder_name)
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)

txt = open("titles.txt","r")
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


ydl_mp3 = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook]
}
ydl_flv = {'format': 'bestvideo[ext=flv]+bestaudio[ext=m4a]/best[ext=flv]/best'}
ydl_m4a = {'format':'140','logger': MyLogger(),'progress_hooks': [my_hook]}

ydl_mkv = {'format': 'bestvideo+bestaudio/best'}
ydl_mp4 = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
}

format_dict={'mp3':ydl_mp3,'flv':ydl_flv,'m4a':ydl_m4a,'mkv':ydl_mkv,'mp4':ydl_mp4}

dl_format = ""
while not dl_format:
    dl_format = input("Pick a format {mp3,m4a,mkv,flv,mp4} : ")
    if not dl_format in format_dict:
        print("Invalid input. Please pick a valuable format")
        dl_format=""




with youtube_dl.YoutubeDL(format_dict[dl_format]) as ydl:
    try:
        ydl.download(urls)
    except:pass
