import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


class Video:
    load_dotenv()
    API_KEY = os.environ.get('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id: str):
        try:
            self.video_id = video_id
            self._video = Video.youtube.videos().list(part='snippet,statistics', id=video_id).execute()
            self.title = self._video['items'][0]['snippet']['title']
            self.url = self._video['items'][0]['snippet']['thumbnails']['default']['url']
            self.view_count = self._video['items'][0]['statistics']['viewCount']
            self.likes_count = self._video['items'][0]['statistics']['likeCount']
        except IndexError:
            self._video = None
            self.title = None
            self.url = None
            self.view_count = None
            self.likes_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, plv_id):
        super().__init__(video_id)
        self.plv_id = plv_id

    def __str__(self):
        return self.title
