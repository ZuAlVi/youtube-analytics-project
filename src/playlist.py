import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    __api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, playlist_id):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.playlist_videos = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                                     part='snippet, contentDetails, id, status',
                                                                     maxResults=50,
                                                                     ).execute()
        self.playlist_info = PlayList.youtube.playlists().list(part='snippet',
                                                               id=playlist_id,
                                                               maxResults=50,
                                                               ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        """Метод возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()
        total_time = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration

        return total_time
