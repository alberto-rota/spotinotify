# Shows a user's playlists (need to be authenticated via oauth)

import sys
from pynput import keyboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from windows_toasts import WindowsToaster, ToastImageAndText2, AudioSource, ToastAudio
from win11toast import toast



import requests
from pprint import pprint

def new_toast(title,artist,album):
    wintoaster = WindowsToaster('Currently listenting to:')
    toast = ToastImageAndText2()
    toast.SetHeadline(title)
    toast.SetBody(artist + ' - '+ album)
    toast.SetImage("currentplayed.jpg")
    toast.audio = ToastAudio(AudioSource.IM, looping=True)
    toast.audio.silent = True
    wintoaster.show_toast(toast)

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    # print("Whoops, need a username!")
    # print("usage: python user_playlists.py [username]")
    username = "alberto_rota"
    # sys.exit()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="35b3aaa72edd47f3861f652311162eb6", 
    client_secret="2936833e47af4c77b3d7561da83b415c",
    redirect_uri="http://127.0.0.1:9090",
    scope="user-modify-playback-state user-read-playback-state user-read-currently-playing",
    open_browser=False,
))

previous = sp.current_user_playing_track()
while True:
    current = sp.current_user_playing_track()
    title = current["item"]["name"]
    artist = current["item"]["artists"][0]["name"]
    album = current["item"]["album"]["name"] 
    cover_url = current["item"]["album"]["images"][1]["url"]
    img_data = requests.get(cover_url).content
    with open('currentplayed.jpg', 'wb') as handler:
        handler.write(img_data)

    print(f"Currently playing: {title} by {artist} on {album}")
    
    if previous["item"]["name"] != title and previous["item"]["artists"][0]["name"] != artist and previous["item"]["album"]["name"] != album: 
        new_toast(title,artist,album)
        
    previous = current

# while True:
#     print(sp.current_playback())
#     client_id="35b3aaa72edd47f3861f652311162eb6", 
#     client_secret="2936833e47af4c77b3d7561da83b415c"))
