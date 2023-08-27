import os
import json
import isodate

from datetime import timedelta
from src.video import Video
from googleapiclient.discovery import build



api_key: str = os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList():


  def __init__(self, play_list_id):
      self.play_list_id = play_list_id
      self.play_list_info = youtube.playlistItems().list(playlistId=self.play_list_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute()
      self.video_ids = [video['contentDetails']['videoId'] for video in self.play_list_info['items']]

      self.video_response_time = youtube.videos().list(part='contentDetails,statistics',
                                                  id=','.join(self.video_ids)
                                                  ).execute()
      self.video_response_all = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=self.video_ids
                                                 ).execute()
      self.title = self.video_response_all['items'][0]['snippet']['title']
      self.like_count = self.video_response_all['items'][0]['statistics']['likeCount']
      self.url = f"https://www.youtube.com/playlist?list={self.play_list_id}"



  def total_duration(self):
      timeList = []
      mysum = timedelta()
      for video in self.video_response_time['items']:
          iso_8601_duration = video['contentDetails']['duration']
          duration = (isodate.parse_duration(iso_8601_duration))
          timeList.append(str(duration))
      for i in timeList:
          (h, m, s) = i.split(':')
          d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
          mysum += d
      return(mysum)



  def show_best_video(self):
      popular = [video['statistics']['likeCount'] for video in self.video_response_all['items']]
      best = (max(popular))
      for item in self.video_response_all["items"]:
          if item['statistics']['likeCount'] == best:
              return f'https://youtu.be/{item["id"]}'






