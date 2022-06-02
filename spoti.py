import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="c7e5f0281614491c8e25f7c2f7cce02d",
                                               client_secret="03431fa0d032434fa6d91699ad17394e",
                                               redirect_uri="http://localhost:8888",
                                               scope="user-library-modify, user-read-playback-state, user-library-read, user-read-private, playlist-read-private, playlist-modify-private, playlist-modify-public, user-read-recently-played"))

playlist_id = "71DDAcK9LAdJ9glbqnlInx"
repetitions = 3

# merge two dictionaries together
def merge_dicts(dict1, dict2):
  res = {**dict1, **dict2}
  return res

# pretty prints songs in playlist
def pretty_print_songs(songs):
  print(json.dumps(songs, indent=4))

def get_all_songs_of_playlist_helper(playlist_id, ofs=0):
    results = sp.user_playlist_tracks(user=sp.me()["id"], playlist_id=playlist_id, offset=100*ofs, fields="items")
    songs = {}
    for item in results["items"]:
      songs[item["track"]["name"]] = item["track"]["id"]
    return songs

def all_playlist_songs(playlist_id, repetitions):
  all_songs = {}
  for i in range(repetitions):
    more_songs = get_all_songs_of_playlist_helper(playlist_id, i)
    all_songs = merge_dicts(all_songs, more_songs)
  return all_songs

def add_tracks_to_playlist(playlist_id, songs):
  sp.user_playlist_add_tracks(user=sp.me()["id"], playlist_id=playlist_id, tracks=songs.values())

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
pretty_print_songs(all_liked_songs)
pretty_print_songs(all_current_playlist_songs)

# add_tracks_to_playlist(playlist_id, songs)

# # after
# pretty_print_songs(all_playlist_songs(playlist_id, repetitions))


# for i in range(5):
#   res2 = sp.current_user_saved_tracks(offset=i*20)
#   for item in res2["items"]:
#     if item["track"]["name"] == "rockstar (feat. 21 Savage)":
#       print("Found song.")
#       time.sleep(5)
#       sp.current_user_saved_tracks_delete(tracks=[item["track"]["id"]])
#       print("Song deleted.")