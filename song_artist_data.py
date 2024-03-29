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

def get_track_features(track_id, sp):
    """
    Retrieve audio features for a track from the Spotify API.

    This function utilizes time.sleep() to prevent hitting API rate limits.

    Args:
        track_id: a string representing the unique identifier for the song.
        sp: an authenticated instance of the Spotipy client.

    Returns:
        A dictionary containing audio features of the track obtained from the 
        Spotify API. If the track features are unavailable or if an error 
        occurs, returns None.
    """
    time.sleep(10) # sleep to prevent hitting spotify api rate limits
    features = sp.audio_features(track_id)

    return features[0]

def find_average(list):
    """
    Finds the average or mode of a list. 
    
    If the list contains all number (int or float), the function finds mean, 
    and if values are strings, the function uses mode
    
    Args:
        list : a list containing numeric or string values.

    Returns:
        An average if the list's elements are numeric, and a string of the 
        mode if the list's elements are strings.

    """
    if len(list) > 0:
        if isinstance(list[0], (float, int)): # using mean
            return sum(list) / len(list)
        if isinstance(list[0], str): # using mode
            counts = {value:0 for value in list}

            for value in list:
                counts[value] += 1

            max_value = max(counts.values())

            for key, value in counts.items():
                if value == max_value:
                    return key

features_to_include = [
    "song_name",
    "artist_name",
    "acousticness",
    "instrumentalness",
    "speechiness",
    "valence"
]

def get_artist_average_features(top_songs, sp):
    """
    Retrieve and compute the average audio features for an artist's top songs.

    Iterates through the list of top songs for an artist, retrieves their 
    audio features using the Spotify API, and calculates the average of each 
    feature across all songs for each artist.

    This function utilizes time.sleep() to avoid hitting API rate limits.
    
    The function depends on the get_track_features and find_average functions.
    
    Args:
        top_songs: a list of dictionaries containing information about the 
            artist's top songs, including a "track_id".
        sp: an authenticated instance of the Spotipy client.

    Returns:
        A dictionary containing the average audio features for the artist's 
        top songs. The keys are the audio features ("acousticness", 
        "instrumentalness", "speechiness", and "valence"), and the values 
        represent the artist's respective average values of their top songs.
    """
    artist_song_features = {}
    for song in top_songs:
        time.sleep(5)
        song_features = get_track_features(song["track_id"], sp)
        for key, value in song_features.items():
            if key not in features_to_include:
                continue

            existing_values = artist_song_features.get(key)

            if existing_values is None:
                existing_values = []
                artist_song_features[key] = existing_values

            existing_values.append(value)

    average_features = {
        k:find_average(v) for k, v in artist_song_features.items()
    }
    return average_features

def write_data_to_csv(artists_features, file_name, keys=features_to_include):
    """
    Write artist features to a CSV file.

    This function takes a dictionary of artist features generated from 
    get_artist_average_features(). It writes this data to a CSV file.

    The function excludes certain keys ("type", "id", "uri", "track_href", 
    "analysis_url") from the data that are not applicable for analysis before 
    writing to the CSV file.
    
    Each row in the CSV file represents an artist, and columns corresponds 
    to their feature values.

    Args:
        artists_features: a dictionary where the keys are artist names and the 
            values are dictionaries containing feature information. The nested 
            dictionary contains the feature name as a key, and the data as a 
            value.
            
        file_name: the name of the CSV file to write the data to.

    Returns:
        None.
    """
    exclude = ["type", "id", "uri", "track_href", "analysis_url"]

    data = {
        artist_name: {
            k:v for k, v in features.items() if k not in exclude
        } for artist_name, features in artists_features.items()
    }

    data = [{
        "artist_name": artist_name,
        **features
    } for artist_name, features in data.items()]


    with open(file_name, 'w+', newline='', encoding="utf-8") as file:
        dict_writer = csv.DictWriter(file, keys + ["artist_name"])
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    client_credentials_manager = SpotifyClientCredentials(
                                    client_id=api_keys.CLIENT_ID,
                                    client_secret=api_keys.CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artist_names = ['The Weeknd', 'Taylor Swift', 'Ariana Grande', 'Rihanna',
                    'Drake', 'Kanye West', 'Justin Bieber', 'Dua Lipa', 
                    'Coldplay', 'Bruno Mars']

    artists_features = {}
    artists_songs = []

    for artist_name in artist_names:
        top_songs = get_artist_top_songs(artist_name, sp)
        artists_songs.extend(top_songs)
        artists_features[artist_name] = get_artist_average_features(
                                                                top_songs, sp)

    write_data_to_csv(artists_features, "artists_average.csv")
    write_data_to_csv(artists_songs, "artists_songs.csv")