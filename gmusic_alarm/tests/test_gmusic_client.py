from unittest import TestCase
from unittest.mock import Mock

from gmusic_alarm import gmusic_client


class TestGmusicClient(TestCase):

    def setUp(self):
        config_parser_mock = gmusic_client.configparser.ConfigParser
        config_parser_mock.read = Mock()

        fake_username = 'foo@gmail.com'
        fake_password = 'secretpw'

        def mock_config_get(*args):
            if 'username' in args:
                return fake_username
            if 'password' in args:
                return fake_password
        config_parser_mock.get = Mock(side_effect=mock_config_get)

        self.gclient = gmusic_client.GClient()

    def test_get_device_id(self):
        mobileclient_mock = gmusic_client.Mobileclient
        fake_registered_devices = [{'kind': 'sj#devicemanagementinfo',
                                    'id': '0x12345',
                                    'type': 'ANDROID',
                                    'friendlyName': 'Super Fake Phone',
                                    'lastAccessedTimeMs': '1478446463844'}]
        mock_kwargs = {'return_value': fake_registered_devices}
        mobileclient_mock.get_registered_devices = Mock(**mock_kwargs)
        self.assertEqual(self.gclient.get_device_id(), '12345')

    def test_get_station(self):
        mobileclient_mock = gmusic_client.Mobileclient
        fake_station_1 = {'inLibrary': False, 'id': 'station1'}
        fake_station_2 = {'inLibrary': True, 'id': 'station2'}
        fake_station_3 = {'inLibrary': False, 'id': 'station3'}
        fake_stations = [fake_station_1, fake_station_2, fake_station_3]
        mobileclient_mock.get_all_stations = Mock(return_value=fake_stations)
        self.assertEqual(self.gclient.get_station(), fake_station_2)
