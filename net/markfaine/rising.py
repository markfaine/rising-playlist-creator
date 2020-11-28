#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pickle
import argparse
import logging
import logging.config
import logging.handlers
from datetime import datetime
from net.markfaine.reddit import RisingPlaylist
from net.markfaine.mygoogle import GoogleService
from net.markfaine.youtube import PlaylistManager

__author__ = "Mark Faine"
__email__ = "mark.faine@nasa.gov"
__maintainer__ = "Mark Faine"

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Default logger
logger = logging.getLogger(__name__)

# Youtube API configuration
# You'll have to setup an application at console.google.com and download
# cliet_secret_file.json
CLIENT_SECRET_FILE  =  'client_secret_file.json'
API_NAME  =  'youtube'
API_VERSION  =  'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Reddit API Configuration
# You need to add your information here
REDDIT_CLIENT_ID = ''
REDDIT_SECRET_KEY = ''

def defaults(args):
    configure_logging(args)
    logger.debug("Configuring defaults")
    logger.debug(f"Args: {args}")
    if not args.date:
        date = datetime.now()
    else:
        date = datetime.strptime(args.date, '%m/%d/%y')
    global str_date
    str_date = date.strftime('%B %d, %Y')
    logger.debug(f"Date: {str_date}")

def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(prog="rising-playlist-creator",
                                     description="Add a Rising playlist to your Youtube account")
    # Debugging
    parser.add_argument('--debug', action='store_true', default=False, help="Enable debug logging")

    # Delete
    parser.add_argument('--delete', action='store_true', default=False, help="Just delete your playlist with this date, if found")

    # The date
    parser.add_argument('date', action='store', nargs='?', type=str, help="Optional date of the playlist to add,\
         default is today and the format is mm/dd/yy")

    # Defaults
    parser.set_defaults(func=defaults)

    return parser.parse_args()

def configure_logging(args):
    logger = logging.getLogger()
    logging.basicConfig(format='"%(asctime)s - %(name)s - %(levelname)s \
                        - %(message)s"',
                        level=logging.INFO)
    logger.info("Configuring logging")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    logger.info(f"Starting logging at {datetime.now()} ")


def delete_playlist(service):
    playlistManager = PlaylistManager(service)
    target_playlist_id = playlistManager.find_playlist(f"Rising {str_date}")
    if target_playlist_id:
        logger.debug(f"Target Playlist ID: {target_playlist_id}")
        playlistManager.delete_playlist(target_playlist_id)


def create_playlist(service):
    rising = RisingPlaylist(REDDIT_CLIENT_ID, REDDIT_SECRET_KEY, str_date)
    src_playlist_id = rising.get_playlist_id()
    logger.debug(f"Source Playlist ID: {src_playlist_id}")
    playlistManager = PlaylistManager(service)
    target_playlist = playlistManager.create_playlist(f"Rising {str_date}")
    target_playlist_id = target_playlist['id']
    if target_playlist_id:
        logger.debug(f"Target Playlist ID: {target_playlist_id}")
        source_playlist = playlistManager.copy_playlist(src_playlist_id, target_playlist_id)

def main():
    import sys
    args = parse_args()
    args.func(args)

    # delete or create playlist
    service = GoogleService(CLIENT_SECRET_FILE, SCOPES, API_NAME, API_VERSION).authenticate()
    if args.delete:
        delete_playlist(service)
    else:
        create_playlist(service)

if __name__ == "__main__":
    main()

