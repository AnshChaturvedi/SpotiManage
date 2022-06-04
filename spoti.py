import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
from dotenv import load_dotenv
import os

# get environment variables
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))

playlist_id = "71DDAcK9LAdJ9glbqnlInx"
repetitions = 3

# no error checking at the moment, thats a work in progress
def extract_playlist_id(spotify_url):
  beg = "https://open.spotify.com/playlist/"
  spotify_url = spotify_url.replace(beg, "")

  index = 0
  str_len = len(spotify_url)
  for i in range(str_len):
    if spotify_url[i] == "?":
      index = i
      break
  
  spotify_url = spotify_url[:index]
  return spotify_url

# merge two dictionaries together
def merge_dicts(dict1, dict2):
  res = {**dict1, **dict2}
  return res

# pretty prints songs in playlist
def pretty_print(songs):
  print(json.dumps(songs, indent=4))
  
def all_playlist_songs(playlist_id, repetitions):
  all_songs = {}
  for i in range(repetitions):
    more_songs = get_all_songs_of_playlist_helper(playlist_id, i)
    all_songs = merge_dicts(all_songs, more_songs)
  return all_songs

def get_all_songs_of_playlist_helper(playlist_id, ofs=0):
    results = sp.user_playlist_tracks(user=sp.me()["id"], playlist_id=playlist_id, offset=100*ofs, fields="items")
    songs = {}
    for item in results["items"]:
      songs[item["track"]["name"]] = item["track"]["id"]
    return songs


def add_tracks_to_playlist(playlist_id, liked_songs):
  sp.user_playlist_add_tracks(user=sp.me()["id"], playlist_id=playlist_id, tracks=liked_songs.values())

def get_all_liked_songs():
  songs = {}
  for i in range(5):
    results = sp.current_user_saved_tracks(limit=50, offset=50*i)
    for item in results["items"]:
      songs[item["track"]["name"]] = item["track"]["id"]
  return songs

all_liked_songs = get_all_liked_songs()
all_current_playlist_songs = all_playlist_songs(playlist_id, repetitions)

# before
pretty_print(all_liked_songs)
pretty_print(all_current_playlist_songs)
print("adding songs...")

# after
time.sleep(10)
add_tracks_to_playlist(playlist_id, all_liked_songs)
pretty_print(all_playlist_songs(playlist_id, repetitions))


# for i in range(5):
#   res2 = sp.current_user_saved_tracks(offset=i*20)
#   for item in res2["items"]:
#     if item["track"]["name"] == "rockstar (feat. 21 Savage)":
#       print("Found song.")
#       time.sleep(5)
#       sp.current_user_saved_tracks_delete(tracks=[item["track"]["id"]])
#       print("Song deleted.")