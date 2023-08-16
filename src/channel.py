import json
import os
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']


    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube


    def to_json(self, name):
        with open('moscowpython.json', 'a') as file:
            json.dump(self.channel_info, file)


    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel_info = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel_info, indent=4, ensure_ascii=False))


