from setuptools import setup

setup(
    name='gmusic-alarm',
    version='0.0.1',
    description='Alarm clock using Google Play Music radio stations',
    url='https://github.com/cmurphy/gmusic-alarm',
    author='Colleen Murphy',
    author_email='colleen@gazlene.net',
    license='Apache-2.0',
    packages=['gmusic_alarm'],
    install_requires=['gmusicapi', 'python-vlc'],
    entry_points={
        'console_scripts': ['gmusic-alarm=gmusic_alarm.cli:run'],
    }
)
