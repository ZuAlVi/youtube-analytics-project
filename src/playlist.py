import os

from googleapiclient.discovery import build


class PlayList:
    __api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)
