from __future__ import unicode_literals
import os
import requests
import youtube_dl
from googleapiclient.discovery import build
import tkinter as tk
import webbrowser

## OPTIONS

api_key = 'AIzaSyDXgMiUhVLW4Ls0dDnKAm_sOXc4gzRK7aQ'
folder_name = 'music'
max_videos_in_playlist = 20 #the limit set by youtube is 50 videos
search_by_popularity = True

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

class Can:
    def __init__(self,video):
        self.video = video
        self.cnv = tk.Canvas(window,width=900,height=50,bg='ivory',bd=10)
        self.cnv.pack(padx=10, pady=10)
        self.cnv.create_text(450,25,text=video['snippet']['title'],fill="black")
        self.cnv.bind("<Button-1>",self.click)
    
    def click(self,event):
        webbrowser.open("https://www.youtube.com/watch?v=" + self.video['id']['videoId'])

def search_vid(word):
    request = youtube.search().list(q=word, part='snippet', order='viewCount' if search_by_popularity else None, maxResults=10
    , type='video')
    response = request.execute()
    for video in response['items']:
        videos.append(Can(video))

def search_playlists(word):
    url_list = []
    request = youtube.search().list(q=word, part='snippet',order='viewCount' if search_by_popularity else None, maxResults=20, type='playlist')
    response = request.execute()
    searched_playl = response['items'][0]['id']['playlistId']
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

def search(event):
    search_vids_n_playls(user_input.get())


os.chdir(os.path.dirname(os.path.abspath(__file__)))
create_folder(folder_name)
youtube = build('youtube', 'v3', developerKey=api_key)

window = tk.Tk()
user_input = tk.StringVar(window)
text_box = tk.Entry(window,textvariable=user_input)
text_box.pack(side=tk.LEFT)
text_box.bind('<Return>',search)
videos = []

window.mainloop()