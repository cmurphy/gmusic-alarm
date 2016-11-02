import os
import json
import time

import configparser
from contextlib import redirect_stderr

from gmusicapi import Mobileclient
import vlc

CREDENTIALS_FILE = '~/.gmusic-alarm-creds'

def get_credentials():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CREDENTIALS_FILE))
    credentials = {}
    credentials['username'] = config.get('credentials', 'username')
    credentials['password'] = config.get('credentials', 'password')
    return credentials

def login(gclient):
    credentials = get_credentials()
    logged_in = gclient.login(credentials['username'],
                              credentials['password'],
                              Mobileclient.FROM_MAC_ADDRESS)
    if not logged_in:
        print("Failed to log in.")
        exit(1)

def get_device_id(gclient):
    # Get all devices, pick the first one, get its ID, strip the leading '0x'
    device_id = gclient.get_registered_devices()[0]['id'][2:]
    return device_id

def get_station(gclient):
    stations = [station for station in gclient.get_all_stations()
                if station['inLibrary']]
    return stations[0]

def get_tracks(gclient, stations):
    tracks = gclient.get_station_tracks(stations['id'])
    return tracks

def play_tracks(gclient, tracks):
    device_id = get_device_id(gclient)
    vlc_client = vlc.Instance('--file-caching 3000')
    player = vlc_client.media_player_new()
    # The MediaList type doesn't understand streams properly, so we need to
    # get the song length from the gmusicapi data and use that to stop the
    # player and start the next song using just the Media type.
    for track in tracks:
        duration = int(track['durationMillis'])
        stream_url = gclient.get_stream_url(track['nid'],
                                            device_id=device_id)
        media = vlc_client.media_new(stream_url)
        player.set_media(media)
        # +3000 - Give laggy songs extra time to finish
        end_time = time.time() * 1000 + duration + 3000
        while time.time() * 1000 < end_time:
            player.play()

def main():
    gclient = Mobileclient()
    login(gclient)
    station = get_station(gclient)
    tracks = get_tracks(gclient, station)
    play_tracks(gclient, tracks)

if __name__ == '__main__':
    main()
