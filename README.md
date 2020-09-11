# DlMusicFromYt
This is a script which allows you to download a high number of music from youtube for free.
You just have to have the text_file.txt in the same folder, and to write in it titles of videos you want from youtube (line by line), and the script will search for them on youtube, and download them.
If you add "playlist" at the beginning of a line, the script will ask you if you want to the dl the playlist it found, and then dl the vids from the playlist (the youtube api sets the limit to 50 videos per playlist).
All files downloaded will be placed in a new folder in your cwd (the folder in which is the script).

Right now, you can only download mp3 in 256kBs (which is pretty good).

# Requirements
* [An API youtube v3 key without login](https://developers.google.com/youtube/registering_an_application)
* google-api-python-client and youtube_dl modules (type the command ``python -m pip install google-api-python-client`` then ``python -m pip install youtube_dl``in your terminal)
* a file named  text_file.txt in the same folder as the python file

There is an example of a text_file.txt correctly written on this git
