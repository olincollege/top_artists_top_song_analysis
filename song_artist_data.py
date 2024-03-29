"""
Functions to query song features for selected songs and write the data into
.csv files.
"""
from __future__ import print_function
import csv
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import api_keys

def get_artist_top_songs(artist_name, sp):
    """
    Finds the Spotify ID of the top ten artists by active listeners and
    gathers information of every artists' top ten most popular songs with the
    help of Spotipy library. Collects all data in one list.

    Args:
        artist_name: a string representing the name of the artist to search.
        sp: a function from Spotipy that manages client credential information
            necessary for accessing the API.
    
    Returns:
        A list with general information of the top ten songs of the ten 
        most popular artists.
    """
    tracks_info = []
    all_tracks_info = []

    #search for artist
    results = sp.search(q='artist:' + artist_name, type='artist')
    if len(results['artists']['items']) == 0:
        print(f"No artist found with the name '{artist_name}'.")
        return

    #get artist ID
    artist_id = results['artists']['items'][0]['id']

    #get top tracks
    time.sleep(10)
    top_tracks = sp.artist_top_tracks(artist_id)

    #extract information
    for track in top_tracks['tracks']:
        track_info = {
            'artist_name': artist_name,
            'name': track['name'],
            'track_id': track['id'],
            'popularity': track['popularity'],
            'album_name': track['album']['name'],
            'album_release_date': track['album']['release_date'],
        }
        tracks_info.append(track_info)
    all_tracks_info.extend(tracks_info)

    return all_tracks_info
