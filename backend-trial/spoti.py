import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
from dotenv import load_dotenv
import os
from itertools import islice
from pprint import pprint
from timeit import default_timer as timer

# get environment variables
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))

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


# creates an iterable generator to split songs into chunks
def chunks(data, SIZE=10000):
  it = iter(data)
  for i in range(0, len(data), SIZE):
      yield {k:data[k] for k in islice(it, SIZE)}

# returns list of dictionaries with `x` songs per dictionary
def break_songs_into_chunks(songs: dict, chunk_size: int) -> list:
  total_songs = []
  for item in chunks({i:songs[i] for i in songs}, chunk_size):
    total_songs.append(item) 

  return total_songs

# get all songs of playlist
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

# add songs to playlist
def add_tracks_to_playlist(playlist_id: str, songs: list):
  for chunk in songs:
    sp.user_playlist_add_tracks(user=sp.me()["id"], playlist_id=playlist_id, tracks=chunk.values())

def get_all_liked_songs():
  songs = {}
  for i in range(5):
    results = sp.current_user_saved_tracks(limit=50, offset=50*i)
    for item in results["items"]:
      songs[item["track"]["name"]] = item["track"]["id"]
  return songs

# liked to playlist
def testing():
  # test1 playlist
  playlist_link = "https://open.spotify.com/playlist/37VuZXo0HrplEBi05klcMv?si=4667000a5684496c"
  playlist_to_add = extract_playlist_id(playlist_link)

  # playlist_id = extract_playlist_id("https://open.spotify.com/playlist/71DDAcK9LAdJ9glbqnlInx?si=e3d945eeff764004")
  repetitions = 1

  all_liked_songs = break_songs_into_chunks(get_all_liked_songs(), 100)
  all_current_playlist_songs = all_playlist_songs(playlist_to_add, repetitions)

  # before
  pretty_print(all_liked_songs)
  time.sleep(5)
  pretty_print(all_current_playlist_songs)
  print("adding songs...")

  # after
  add_tracks_to_playlist(playlist_to_add, all_liked_songs)
  time.sleep(5)
  print("added songs.")
  pretty_print(all_playlist_songs(playlist_to_add, repetitions))


# playlist to playlist
def another_test():
  start = timer()
  _from = "https://open.spotify.com/playlist/71DDAcK9LAdJ9glbqnlInx?si=51b0cf0a69eb4b9b"
  _to = "https://open.spotify.com/playlist/52Hh2G8ENMmF3tNc1QpsM2?si=256298268d4c488f"

  from_id = extract_playlist_id(_from)
  to_id = extract_playlist_id(_to)
  repetitions = 5

  all_from_songs = break_songs_into_chunks(all_playlist_songs(from_id, repetitions), 100)
  all_to_songs = all_playlist_songs(to_id, repetitions)

  add_tracks_to_playlist(to_id, all_from_songs)
  end = timer()
  print("Done, took " + str(end - start) + " seconds")

# another_test()
