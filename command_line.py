from __future__ import unicode_literals
import os
import requests
import youtube_dl
from googleapiclient.discovery import build

## OPTIONS

api_key = ''
folder_name = 'music'
max_videos_in_playlist = 20 #the limit set by youtube is 50 videos
search_by_popularity = False # if set to false, it will search by relevance

## OPTIONS

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
    print("Download " + searched_vid)
    print("video ---> " + response['items'][0]['snippet']['title'])
    return [searched_vid]

def search_playlists(word):
    request = youtube.search().list(q=word, part='snippet',order='viewCount' if search_by_popularity else None, maxResults=1, type='playlist')
    response = request.execute()
    searched_playl = response['items'][0]['id']['playlistId']
    return get_from_playlist(searched_playl)
    
def get_from_playlist(searched_playl):
    url_list = []
    request = youtube.playlistItems().list(part='snippet', playlistId=searched_playl, maxResults=max_videos_in_playlist)
    response = request.execute()
    for video in response['items']:
        vid_url = "https://www.youtube.com/watch?v=" + video['snippet']['resourceId']['videoId']
        url_list.append(vid_url)
    print("Download https://www.youtube.com/playlist?list=" + searched_playl)
    for video in response['items']:
        print("video ---> " + video['snippet']['title'])
    return url_list

def search_vids_n_playls(line):
    if "https://www.youtube.com/playlist?list=" in line:
        return get_from_playlist(line)
    elif "https://www.youtube.com/watch?v=" in line:
        return [line]
    elif "playlist" in line:
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
youtube = build('youtube', 'v3', developerKey=api_key)
create_folder(folder_name)

line = input("Search for title of a vid, or a playlist: ")

while not line == "":
    urls = search_vids_n_playls(line)

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
