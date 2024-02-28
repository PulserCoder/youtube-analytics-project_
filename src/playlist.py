import datetime
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


class PlayList:
    load_dotenv()
    API_KEY = os.environ.get('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id: int):
        self.playlist_id = playlist_id
        self.playlist = PlayList.youtube.playlists().list(part="snippet", id=playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        playlist_all_items = PlayList.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
            maxResults=50
        ).execute()
        seconds_count = 0
        for item in playlist_all_items['items']:
            video_id = item['contentDetails']['videoId']
            video_info = PlayList.youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()

            video_duration = video_info['items'][0]['contentDetails']['duration']
            parsed_duration = self.parse_duration(video_duration)
            seconds_count += parsed_duration.total_seconds()

        return datetime.timedelta(seconds=seconds_count)

    def parse_duration(self, duration_str):
        duration = datetime.timedelta()
        time_parts = duration_str.split('T')
        if len(time_parts) == 2:
            if "H" in time_parts[1]:
                hours, rest = time_parts[1].split("H")
                duration += datetime.timedelta(hours=int(hours))
                time_parts[1] = rest
            if 'M' in time_parts[1]:
                minutes, rest = time_parts[1].split("M")
                duration += datetime.timedelta(minutes=int(minutes))
                time_parts[1] = rest
            if "S" in time_parts[1]:
                seconds = time_parts[1].replace("S", "")
                duration += datetime.timedelta(seconds=int(seconds))

        return duration

    def show_best_video(self):

        playlist_allitems = PlayList.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
            maxResults=50
        ).execute()

        best_video_url = ''
        max_likes_count = 0

        for item in playlist_allitems['items']:
            video_id = item['contentDetails']['videoId']
            video_info = PlayList.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            total_likes = int(video_info['items'][0]['statistics']['likeCount'])
            if total_likes > max_likes_count:
                max_likes_count = total_likes
                best_video_url = f"https://youtu.be/{video_id}"

        return best_video_url
