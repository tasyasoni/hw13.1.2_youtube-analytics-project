import os
import json
from googleapiclient.discovery import build



class Video:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel_info = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.channel_id
                                           ).execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']
        self.like_count = self.channel_info['items'][0]['statistics']['likeCount']


    def __str__(self):
        return f"{self.title}"

class PLVideo(Video):

    def __init__(self, channel_id, play_list_id: str) -> None:
        super().__init__(channel_id)
        self.play_list_id = play_list_id
        self.play_list_info = playlist_videos = self.youtube.playlistItems().list(playlistId=self.play_list_id,
                                                   part='contentDetails',
                                                   maxResults=50,
                                                   ).execute()


