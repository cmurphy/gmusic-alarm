import os
import configparser

from gmusicapi import Mobileclient

CREDENTIALS_FILE = '~/.gmusic-alarm-creds'


class GClient:

    def __init__(self):
        self._gclient = Mobileclient()
        self._credentials = self._get_credentials()

    def _get_credentials(self):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(CREDENTIALS_FILE))
        credentials = {}
        credentials['username'] = config.get('credentials', 'username')
        credentials['password'] = config.get('credentials', 'password')
        return credentials

    def login(self):
        logged_in = self._gclient.login(self._credentials['username'],
                                        self._credentials['password'],
                                        Mobileclient.FROM_MAC_ADDRESS)
        if not logged_in:
            print("Failed to log in.")
            exit(1)

    def get_device_id(self):
        # Get all devices, pick the first, get its ID, strip the leading '0x'
        self.device_id = self._gclient.get_registered_devices()[0]['id'][2:]
        return self.device_id

    def get_station(self):
        stations = [station for station in self._gclient.get_all_stations()
                    if station['inLibrary']]
        return stations[0]

    def get_tracks(self):
        station = self.get_station()
        tracks = self._gclient.get_station_tracks(station['id'])
        return tracks

    def get_stream_url(self, track_id):
        device_id = self.get_device_id()
        return self._gclient.get_stream_url(track_id, device_id)
