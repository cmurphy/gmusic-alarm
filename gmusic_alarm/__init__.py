import sys
import time

import vlc

from gmusic_alarm import gmusic_client


def play_tracks(gclient, tracks, verbose):
    vlc_client = vlc.Instance('--file-caching 3000 --aout=ALSA')
    player = vlc_client.media_player_new()
    # The MediaList type doesn't understand streams properly, so we need to
    # get the song length from the gmusicapi data and use that to stop the
    # player and start the next song using just the Media type.
    for track in tracks:
        duration = int(track['durationMillis'])
        title = track['title']
        artist = track['artist']
        stream_url = gclient.get_stream_url(track['nid'])
        media = vlc_client.media_new(stream_url)
        player.set_media(media)
        if verbose:
            print('Now playing "{title}" by {artist}'.format(title=title,
                                                             artist=artist))
        player.play()
        while player.get_time() < duration:
            time.sleep(5)


def main():
    gclient = gmusic_client.GClient()
    gclient.login()
    tracks = gclient.get_tracks()
    if '--verbose' in sys.argv or '-v' in sys.argv:
        verbose = True
    else:
        verbose = False
    play_tracks(gclient, tracks, verbose)

if __name__ == '__main__':
    main()
