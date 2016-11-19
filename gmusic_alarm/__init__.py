import time

import vlc

from gmusic_alarm import gmusic_client


def play_tracks(gclient, tracks):
    vlc_client = vlc.Instance('--file-caching 3000')
    player = vlc_client.media_player_new()
    # The MediaList type doesn't understand streams properly, so we need to
    # get the song length from the gmusicapi data and use that to stop the
    # player and start the next song using just the Media type.
    for track in tracks:
        duration = int(track['durationMillis'])
        stream_url = gclient.get_stream_url(track['nid'])
        media = vlc_client.media_new(stream_url)
        player.set_media(media)
        player.play()
        while player.get_time() < duration:
            time.sleep(5)


def main():
    gclient = gmusic_client.GClient()
    gclient.login()
    tracks = gclient.get_tracks()
    play_tracks(gclient, tracks)

if __name__ == '__main__':
    main()
