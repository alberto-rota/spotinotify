# Copyright 2023 alber
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
from pynput import keyboard
import subprocess
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from windows_toasts import WindowsToaster, ToastImageAndText2, AudioSource, ToastAudio
import requests
from rich import print

GET_TRACK_URL="https://api.spotify.com/v1/me/player/currently-playing"
ACCESS_TOKEN="BQCm0b2tI2ymUwPORu0-2qmIp9nAyFC54YBpbOtTJ86jPxxotmz0zLk-E5ymbynYI3koqtLSHec8EuYpp8p90SRcvWDDi-5VklqKOrVHz7IWpfzhTnq3dnCafz9F8Qj8XkoD0br5Xi2cyzKlxq33ybK3bbqQQ36w5M-6TH20VoFPFLqNIXigJAwJ9Cg"

pressed = set()
COMBINATIONS = [
    {
        "keys": [
            {keyboard.Key.cmd, keyboard.KeyCode(char="w")},
        ],
        "command": "next",
    },
    {
        "keys": [
            {keyboard.Key.cmd, keyboard.Key.alt, keyboard.Key.left},
        ],
        "command": "previous",
    },
    
    {
        "keys": [
            {keyboard.Key.cmd, keyboard.Key.space},
        ],
        "command": "pause",
    },
]

def new_toast(title,artist,album):
    wintoaster = WindowsToaster("Currently listenting to:")
    toast = ToastImageAndText2()
    toast.SetHeadline(title)
    toast.SetBody(artist + " - "+ album)
    toast.SetImage("currentplayed.jpg")
    toast.audio = ToastAudio(AudioSource.IM, looping=True)
    toast.audio.silent = True
    wintoaster.show_toast(toast)


def get_current_track(token) -> dict:
    response = requests.get(
        GET_TRACK_URL,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    response_json = response.json()
    try:
        trackdata = {
            "title": response_json["item"]["name"],
            "artist": response_json["item"]["artists"][0]["name"],
            "album": response_json["item"]["album"]["name"],
            "cover_url": response_json["item"]["album"]["images"][1]["url"],
            "error": False,
        }
    except:
        print("[red] Error: " + response_json["error"]["message"])
        return {"error": True, "message": response_json["error"]["message"]}
            
    return trackdata

def response_to_track(response):
    try:
        return {
                "title": response["item"]["name"],
                "artist": response["item"]["artists"][0]["name"],
                "album": response["item"]["album"]["name"],
                "cover_url": response["item"]["album"]["images"][1]["url"],        
                "error": False,
            }
    except:
        return {"error": True , "message": response["message"]}
    
def print_track(track):
    if track["error"]:
        print("[red] No track data" + track["message"])
    print("Title: " + track["title"])
    print("Artist: " + track["artist"])
    print("Album: " + track["album"])

def new_toast(trackdata):
    wintoaster = WindowsToaster("Currently listenting to:")
    toast = ToastImageAndText2()
    toast.SetHeadline(trackdata["title"])
    toast.SetBody(trackdata["artist"] + " - "+ trackdata["album"])
    with open("currentplayed.jpg", "wb") as handler:
        handler.write(requests.get(trackdata["cover_url"]).content)
    toast.SetImage("currentplayed.jpg")
    toast.audio = ToastAudio(AudioSource.IM, looping=True)
    toast.audio.silent = True
    wintoaster.show_toast(toast)


def run(s):
    subprocess.Popen(s)

def on_press(key):
    pressed.add(key)
    for c in COMBINATIONS:
        for keys in c["keys"]:
            if keys.issubset(pressed):
                # run(c["command"])
                print(c["command"])

def on_release(key):
    if key in pressed:
        pressed.remove(key)
        
def playback_next():
    print("next")
def playback_previous():
    print("previous")
def playback_pause():
    print("pause")
def playback_quit():
    print("quit")
    return False

def main():    
    # current_track_info= get_current_track(ACCESS_TOKEN)
    # if not current_track_info["error"]:
    #     print(current_track_info)
    #     new_toast(current_track_info)
    
    username = "alberto_rota"
    scope = "user-read-currently-playing"
    token = util.prompt_for_user_token(username, scope, redirect_uri="http://127.0.0.1:9090")
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playing_track()
    print_track(response_to_track(results))
    new_toast(response_to_track(results))
    
    # return 0 


    with keyboard.GlobalHotKeys({
        "<ctrl_r>+p": playback_next,
        "<ctrl_l>+p" : playback_previous,
        # "<ctrl>+<alt>+<space>": playback_pause,
        # "<ctrl>+<alt>+<esc>"  : playback_quit
    }) as listener:
        listener.join()
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()