import os

import configparser

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
    tracks = gclient.get_station_tracks(stations['id'], num_tracks=1)
    return tracks

def play_tracks(gclient, tracks):
    device_id = get_device_id(gclient)
    vlc_client = vlc.Instance()
    player = vlc_client.media_player_new()
    for track in tracks:
        stream_url = gclient.get_stream_url(tracks[0]['nid'],
                                            device_id=device_id)
        media = vlc_client.media_new(stream_url)
        player.set_media(media)
        while True:
            player.play()

def main():
    gclient = Mobileclient()
    login(gclient)
    station = get_station(gclient)
    tracks = get_tracks(gclient, station)
    play_tracks(gclient, tracks)
