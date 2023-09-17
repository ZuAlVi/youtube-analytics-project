import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    __api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return Channel.youtube

    def to_json(self, name: str):
        temp_dict = {
            '__channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(name, "w", encoding='utf-8') as file:
            json.dump(temp_dict, file, ensure_ascii=False)

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        if isinstance(self, Channel) and isinstance(other, Channel):
            return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        if isinstance(self, Channel) and isinstance(other, Channel):
            return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        if isinstance(self, Channel) and isinstance(other, Channel):
            return int(self.subscriber_count) == int(other.subscriber_count)

    def __gt__(self, other):
        if isinstance(self, Channel) and isinstance(other, Channel):
            return int(self.subscriber_count) > int(other.subscriber_count)

    def __lt__(self, other):
        if isinstance(self, Channel) and isinstance(other, Channel):
            return int(self.subscriber_count) < int(other.subscriber_count)

