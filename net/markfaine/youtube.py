# -*- coding: utf-8 -*-
from net.markfaine.mygoogle import GoogleService
from autoclass import autoclass
from pyfields import field
from googleapiclient.discovery import Resource

import logging

__author__ = "Mark Faine"
__email__ = "mark.faine@gmail.com"
__maintainer__ = "Mark Faine"

# Default logger
logger = logging.getLogger(__name__)

@autoclass()
class PlaylistManager:
    service: Resource = field(check_type=True, doc="The google service")


    def copy_playlist(self, source_id, target_id):
        logger.debug(f"Copying playlist {source_id} to {target_id}")
        response = self.service.playlistItems().list(
            part='contentDetails',
            playlistId=source_id,
            maxResults=50
        ).execute()

        playlistItems = response['items']
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.service.playlistItems().list(
                part='contentDetails',
                playlistId=source_id,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            playlistItems.extend(response['items'])
            nextPageToken = response.get('nextPageToken')

        for video in playlistItems:
            request_body = {
                'snippet': {
                    'playlistId': target_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video['contentDetails']['videoId']
                    }
                }
            }
            self.service.playlistItems().insert(
                part='snippet',
                body=request_body
            ).execute()


    def find_playlist(self, title):
        logger.debug(f"Searching for playlist with title: {title}")
        response = self.service.playlists().list(
            part='snippet',
            mine=True,
            maxResults=50
        ).execute()

        playlistItems = response['items']
        nextPageToken = response.get('nextPageToken')

        for item in playlistItems:
            logger.debug(f"Item: {item['snippet']['title']}")
            if item['snippet']['title'] == title:
                logger.debug(f"Id: {item['id']}")
                return item['id']


    def create_playlist(self, title):
        logger.debug(f"Create playlist with title: {title}")
        request = self.service.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": title,
            "description": "Rising playlist",
            "tags": [
              "Rising",
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
        )
        response = request.execute()
        logger.debug(f"Response: {response}")
        return response


    def delete_playlist(self, id):
        logger.debug(f"Delete playlist with id: {id}")
        request = self.service.playlists().delete(
            id=id
        )
        response = request.execute()
        logger.debug(f"Response: {response}")
        return response

