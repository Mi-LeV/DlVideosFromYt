# DlMusicFromYt
__WARNING : do NOT download music you don't own or which is not free-to-use__

This is a script which allows you to download a high number of mp3 quickly from youtube videos.
No need to have the URLs, the script will search the videos and playlists by searching them.
# How does it works ?

* Execute command_line.py

The script will :
* Ask you the title of a video or of a playlist
* Search this title of video or of playlist on youtube
* Create a new folder in the folder of the python file (only if not already existing)
* Ask you for the format you want the video to be converted to
* Download this video in the new folder
* And ask you again for a title of a video or of a playlist...

**WINDOW-VERSION COMING SOON !**
(window.py is in progress...)

# Formats
For now, you can download videos in theses formats: mp3,m4a,wav,mp4.
Formats are downloaded in the maximum possible quality.

# Requirements
* [An API youtube v3 key without login](https://developers.google.com/youtube/registering_an_application)
  (the api key already in the code will not work)
* google-api-python-client and youtube_dl modules (type the command ``python -m pip install google-api-python-client`` then ``python -m pip install youtube_dl``in your terminal)
