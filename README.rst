Google Music Alarm
==================

Uses the gmusicapi library and vlc python binding to stream music from a Google
Play Music radio station.

Usage:

This doesn't actually have any alarm clock functionality. It works by setting
up a crontab to run the app, for example::

    30 7 * * 1-5 /path/to/bin/gmusic-alarm

Sets an alarm for 7:30am Monday through Friday. To turn the alarm off, open a terminal, find the process and kill it::

    $ pkill -f gmusic-alarm

You will hopefully be wide awake after this point. Or don't kill the alarm and just rock out.

There's no snooze functionality.

License: Apache 2.0
