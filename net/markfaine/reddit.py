# -*- coding: utf-8 -*-
import praw
import logging
from autoclass import autoclass
from pyfields import field
from datetime import datetime


__author__ = "Mark Faine"
__email__ = "mark.faine@gmail.com"
__maintainer__ = "Mark Faine"

# Default logger
logger = logging.getLogger(__name__)

@autoclass()
class RisingPlaylist:
    client_id: str = field(check_type=True, doc="The client id")
    client_secret: str = field(check_type=True, doc="The client secret")
    date: str = field(check_type=True, doc="The date to search")
    user_agent: str = field(check_type=True, default="rising-playlist-creator by /u/mfaine", doc="The user agent")


    def get_playlist_id(self):
        reddit = praw.Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        user_agent=self.user_agent
        )

        # Get the rising subreddit
        subreddit = reddit.subreddit("rising")
        # look for the submission with the provided date by rising_mod
        # A lot of checks here, probably don't need them all
        for submission in subreddit.new(limit=10):
            logger.debug(f"Title: {submission.title}")
            if submission.title == f"Rising: {self.date}":
                logger.debug(f"Author: {submission.author.name}")
                logger.debug(f"Is Mod: {submission.author.is_mod}")
                if submission.author.is_mod and submission.author.name == 'rising_mod':
                    logger.debug(f"Flair: {submission.link_flair_text}")
                    if submission.link_flair_text == "Weekday Playlist":
                        logger.debug(f"URL: {submission.url}")
                        return submission.url.split('=')[1]
