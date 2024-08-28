from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import requests
import numpy as np


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_track_info(tracks):
    track_info = []
    for track in tracks:
        track_info.append({
            'id': track['id'],
            'name': track['name'],
            'popularity': track['popularity'],
            'artists': [artist['name'] for artist in track['artists']],
            'release_date': track['album']['release_date'],
            'duration': track['duration_ms']
        })
    return pd.DataFrame(track_info)


# source: https://community.spotify.com/t5/Spotify-for-Developers/Too-Many-Requests-429-Error-blocked-for-13-hours/td-p/5664805
def get_audio_features(tracks):
    audio_features = []
    track_ids = [track['id'] for track in tracks]
    
    # divide into chunks to get audio features for 50 tracks at a time
    chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]
    
    for chunk in chunks:
        try:
            results = sp.audio_features(chunk)
            for result in results:
                if result:
                    audio_features.append(add_audio_features(result, is_valid=True))

                # add NaN if current track does not have audio features
                else:
                    print('This track has no audio features!')
                    audio_features.append(add_audio_features(result, is_valid=False))
            time.sleep(1)
        
        # slow down if we are making too many requests from web API (which throws 429 error response)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get('Retry-After', 1))
                print(f"Rate limited. Retrying after {retry_after} seconds.")
                time.sleep(retry_after + 1) 
                continue
            else:
                raise

        except Exception as e:
            print(f"Failed to get audio features for some track IDs: {e}")

    return pd.DataFrame(audio_features)


def add_audio_features(result, is_valid):
    audio_features = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                      'key', 'liveness', 'loudness', 'mode', 'speechiness',
                      'tempo', 'time_signature', 'valence']
    
    return {feature: result[feature] if is_valid else np.nan for feature in audio_features}


def get_random_tracks(year):
    tracks = []
    # search 50 tracks at a time (max limit in spotify API), and repeat for 20 times
    for i in range(0, 20):
        results = sp.search(q=f'year:{year}', type='track', limit=50, offset=i*50)
        tracks.extend(results['tracks']['items'])
    return tracks
    

def main():
    # get 1000 random tracks (per year) between 2000 to 2023
    all_track_info = pd.DataFrame()
    all_audio_features = pd.DataFrame()
    start_year = 2000
    end_year = 2023

    for year in range(start_year, end_year + 1):
        print(f"Getting 1000 random tracks from year {year}:")
        tracks = get_random_tracks(year)
        track_info = get_track_info(tracks)
        audio_features = get_audio_features(tracks)

        all_track_info = pd.concat([all_track_info, track_info])
        all_audio_features = pd.concat([all_audio_features, audio_features])

    # combine track info and audio features horizontally
    all_data = pd.concat([all_track_info, all_audio_features], axis=1)
    
    # output tracks data to csv file
    all_data.to_csv('tracks.csv', index=False)
    

if __name__ == '__main__':
    main()
