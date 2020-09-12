# DlMusicFromYt
__WARNING : do NOT download music you don't own or which is not free-to-use__

This is a script which allows you to download a high number of mp3 from  youtube videos.
No need to have the URLs, the script will search the videos and playlists by searching them.
# How does it works ?

* Open a text file named titles.txt in the same folder.
* Write in it the titles of the videos you want from youtube (1 by line). If you add "playlist" at the beginning of a line, then the script will search for playlists.
* Then execute youtube.py

The script will :
* Read the txt file line by line and take a line as a title of a video or of a playlist (if there is the keyword playlist as the beginning in it).
* search titles of videos on youtube and download them.
* search for titles of playlists on youtube then download all the videos in the playlist found.
* Convert theses videos in mp3 in a new folder in your cwd (the folder in which is the youtube.py executed).

For now, you can only download mp3 in 256kBs (which is pretty good).

# Requirements
* [An API youtube v3 key without login](https://developers.google.com/youtube/registering_an_application)
* google-api-python-client and youtube_dl modules (type the command ``python -m pip install google-api-python-client`` then ``python -m pip install youtube_dl``in your terminal)
* a file named  text_file.txt in the same folder as the python file

There is an example of a titles.txt correctly written in this git.
