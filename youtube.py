from __future__ import unicode_literals
import os
import requests
import youtube_dl
from googleapiclient.discovery import build

api_key = ''
folder_name = 'music'

ydl_mp3 = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }]
}
ydl_m4a = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '256',
    }]
}
ydl_wav = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '256',
    }]
}
ydl_mp4 = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
}

format_dict={'mp3':ydl_mp3,'m4a':ydl_m4a,'wav':ydl_wav,'mp4':ydl_mp4}


def search_vid(word):
    request = youtube.search().list(q=word, part='snippet', order='viewCount' if search_by_popularity else None, maxResults=1, type='video')
    response = request.execute()
    searched_vid = "https://www.youtube.com/watch?v=" + response['items'][0]['id']['videoId']
    print("Download " + searched_vid + response['items'][0]['snippet']['title'])
    return [searched_vid]

def search_playlists(word):
    url_list = []
    request = youtube.search().list(q=word, part='snippet',order='viewCount' if search_by_popularity else None, maxResults=1, type='playlist')
    response = request.execute()
    searched_playl = response['items'][0]['id']['playlistId']
    request = youtube.playlistItems().list(part='snippet', playlistId=searched_playl, maxResults=20)
    response = request.execute()
    for video in response['items']:
        vid_url = "https://www.youtube.com/watch?v=" + video['snippet']['resourceId']['videoId']
        url_list.append(vid_url)
    print(response)
    print("Download https://www.youtube.com/playlist?list=" + searched_playl + response['items'][0]['snippet']['title'])
    return url_list

def search_vids_n_playls(line):
    if "playlist" in line:
        return search_playlists(line[line.find("playlist")+8::])
    else:
        return search_vid(line)

def create_folder(folder_name):
    cwd = os.getcwd()
    new_dir = os.path.join(cwd,folder_name)
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

line = input("Search for title of a vid, or a playlist: ")

while not line == "":
    youtube = build('youtube', 'v3', developerKey=api_key)
    urls = search_vids_n_playls(line)
    create_folder(folder_name)

    dl_format = input("Pick a format {mp3,m4a,wav,mp4} : ")
    while not dl_format in format_dict:
        if dl_format == "":
            break
        print("Invalid input. Please pick a valuable format")
        dl_format = input("Pick a format {mp3,m4a,wav,mp4} : ")
    if not dl_format == "":
        print("DOWNLOADING")
        with youtube_dl.YoutubeDL(format_dict[dl_format]) as ydl:
            try:
                ydl.download(urls)
            except:pass
    else:
        print("Download canceled")
    line = input("Search for title of a vid, or a playlist:")

else:
    print("exiting...")
