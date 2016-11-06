import time

import vlc

import gmusic_alarm.gmusic_client


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
        # +3000 - Give laggy songs extra time to finish
        end_time = time.time() * 1000 + duration + 3000
        while time.time() * 1000 < end_time:
            player.play()

def main():
    gclient = gmusic_client.GClient()
    gclient.login()
    tracks = gclient.get_tracks()
    play_tracks(gclient, tracks)

if __name__ == '__main__':
    main()
