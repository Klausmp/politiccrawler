import ast
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from youtube_transcript_api import YouTubeTranscriptApi

from custom_types import *

def get_latest_videos(api_key: str, channel_id: str) -> list:
    """
    Fetches the latest 10 videos of a given YouTube channel.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        maxResults=10,
        order='date'
    )
    response = request.execute()
    videos = []

    for item in response.get('items', []):
        if item['id'].get('videoId'):
            transcript = ""
            try:
                transcript = str(YouTubeTranscriptApi.get_transcript(item['id']['videoId'], languages=['de']))
            except:
                transcript = ""

            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'transcript': transcript
            })

    print(f"Fetched {len(videos)} videos for channel {channel_id}")
    return videos


def get_video_statistics(api_key: str, video_id: str) -> dict:
    """
    Fetches statistics for a given YouTube video.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()

    if 'items' in response and response['items']:
        statistics = response['items'][0].get('statistics', {})
        stats = {
            'views': int(statistics.get('viewCount', 0)),
            'likes': int(statistics.get('likeCount', 0)),
            'comment_amount': int(statistics.get('commentCount', 0)),
        }
        print(f"Fetched stats for video {video_id}: {stats}")
        return stats

    print(f"No statistics found for video {video_id}")
    return {}


def update_videos(api_key: str, session):
    """
    Retrieves all channels from the database, fetches their latest videos,
    checks if they exist in the database, and updates their statistics.
    """
    channels = session.query(Channel).all()

    for channel in channels:
        print(f"Processing channel: {channel.name} ({channel.channel_id})")
        videos = get_latest_videos(api_key, channel.channel_id)

        for video in videos:
            existing_video = session.query(Youtube_Video).filter_by(video_id=video['video_id']).first()

            if not existing_video:
                new_video = Youtube_Video(
                    name=video['title'],
                    video_id=video['video_id'],
                    transcript=video["transcript"],
                    channelId=channel.id  # Linking video to the correct channel
                )
                session.add(new_video)
                session.commit()
                existing_video = new_video
                print(f"Added new video: {video['title']} ({video['video_id']})")
            else:
                print(f"Video already exists: {video['title']} ({video['video_id']})")

            stats = get_video_statistics(api_key, video['video_id'])

            video_update = Youtube_Video_Update(
                youtube_VideoId=existing_video.id,  # Correct: Uses the proper column name
                views=stats.get('views', 0),
                likes=stats.get('likes', 0),
                comment_amount=stats.get('comment_amount', 0)
            )
            session.add(video_update)
            print(f"Updated stats for video: {video['title']} ({video['video_id']})")

    session.commit()


if __name__ == '__main__':
    load_dotenv(dotenv_path="./.env")
    DATABASE_URL = os.environ.get('DATABASE_URL')

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    api_key = os.environ.get("YT_API_KEY")
    if not api_key:
        raise ValueError("Please set the YT_API_KEY environment variable.")

    update_videos(api_key, session)
