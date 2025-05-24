from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv
import os


# Getting the API key from environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

videos = []
next_page_token = None

# Fetching the currently top 1000 videos from YouTube in France

while len(videos) < 1000:
    request = youtube.videos().list(
        part='snippet,statistics, contentDetails',
        chart='mostPopular',
        regionCode='FR',  # Change as needed
        maxResults=50,
        pageToken=next_page_token
    )
    response = request.execute()
    videos.extend(response['items'])
    next_page_token = response.get('nextPageToken')
    if not next_page_token:
        break


channel_ids = list({v['snippet']['channelId'] for v in videos})

# Fetch subscriber counts for each channel
channel_subs = {}
for i in range(0, len(channel_ids), 50):  # API allows up to 50 ids per request
    ids_chunk = channel_ids[i:i+50]
    channel_request = youtube.channels().list(
        part='statistics',
        id=','.join(ids_chunk)
    )
    channel_response = channel_request.execute()
    for c in channel_response['items']:
        channel_subs[c['id']] = int(c['statistics'].get('subscriberCount', 0))

# Taking all the datas we want from the videos

df = pd.DataFrame([{
    'videoId': v['id'],
    'title': v['snippet']['title'],
    'channelTitle': v['snippet']['channelTitle'],
    'viewCount': v['statistics'].get('viewCount', 0),
    'publishedAt': v['snippet']['publishedAt'],
    'liveBroadcastContent': v['snippet'].get('liveBroadcastContent', 'none'),
    'LikeCount': int(v['statistics'].get('likeCount', 0)),
    'DislikeCount': int(v['statistics'].get('dislikeCount', 0)),
    'CommentCount': int(v['statistics'].get('commentCount', 0)),
    'Duration': v['contentDetails'].get('duration', 'PT0S'),
    'Definition': v['contentDetails'].get('definition', 'unknown'),
    'Caption': v['contentDetails'].get('caption', 'false'),
    'LicensedContent': v['contentDetails'].get('licensedContent', False),
    'ContentRating': v['contentDetails'].get('contentRating', {}),
    'RegionRestriction': v['contentDetails'].get('regionRestriction', {}),
    'subscriberCount': channel_subs.get(v['snippet']['channelId'], None)
} for v in videos[:1000]])

# Putting the data in a CSV

df.to_csv('youtube_top_1000_videos_FR.csv', index=False)