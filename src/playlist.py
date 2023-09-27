import os

from googleapiclient.discovery import build


class PlayList:
    __api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, playlist_id):
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
