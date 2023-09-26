import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource


class Channel:
    """Класс для ютуб-канала"""
    load_dotenv()
    API_KEY = os.environ.get('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel_info = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id = self.channel_info['items'][0]['id']
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = self.channel_info['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> Resource:
        return cls.youtube

    def to_json(self, path):
        with open(path, 'w') as f:
            data = {
                "channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscribers": self.subscriber_count,
                "video_count": self.video_count,
                "views": self.view_count,
            }
            json.dump(data, f, ensure_ascii=False)
