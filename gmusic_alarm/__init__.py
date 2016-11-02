import os

import configparser

from gmusicapi import Mobileclient
import vlc

def main():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.gmusic-alarm-creds'))
    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')

    api = Mobileclient()

    logged_in = api.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
    if not logged_in:
        print("Failed to log in.")
        exit(1)
    device_id = api.get_registered_devices()[0]['id'][2:]
    stations = [station for station in api.get_all_stations() if station['inLibrary']]
    tracks = api.get_station_tracks(stations[0]['id'], num_tracks=1)
    stream_url = api.get_stream_url(tracks[0]['nid'], device_id=device_id)
    print(stream_url)
    vlc_client = vlc.Instance('-v')
    player = vlc_client.media_player_new()
    media = vlc_client.media_new(stream_url)
    player.set_media(media)
    while True:
        player.play()

    print("played a thing")
