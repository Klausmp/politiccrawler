from googleapiclient.discovery import build
from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from custom_types import *
import os
from dotenv import load_dotenv


def get_channel_statistics(api_key: str, channel_id: str) -> dict:
    # Build the YouTube service object
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request the channel statistics
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )

    # Execute the request
    response = request.execute()
    return response


def update_channels(api_key: str, session):
    """
    Retrieves all channels from the database, fetches their statistics from the YouTube API,
    and uploads the results as a new Channel_Update record in the database.
    """
    channels = session.query(Channel).all()
    for channel in channels:
        stats = get_channel_statistics(api_key, channel.channel_id)
        # Ensure we have a valid response with items
        if 'items' in stats and stats['items']:
            statistics = stats['items'][0].get('statistics', {})
            # Get subscriber and view counts; default to 0 if not available.
            subscriber_count = int(statistics.get('subscriberCount', 0))
            view_count = int(statistics.get('viewCount', 0))
            print(f"Updating channel {channel.name}: Subscribers={subscriber_count}, Views={view_count}")
            # Create a new Channel_Update record
            channel_update = Channel_Update(
                channelId=channel.id,
                subscriber=subscriber_count,
                views=view_count
            )
            session.add(channel_update)
        else:
            print(f"No statistics found for channel ID: {channel.channel_id}")
    session.commit()


if __name__ == '__main__':
    load_dotenv(dotenv_path="./.env")

    DATABASE_URL = os.environ.get('DATABASE_URL')

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Ensure tables are created (for demonstration; in production, you should handle migrations properly)
    Base.metadata.create_all(engine)

    # Retrieve your YouTube API key from an environment variable.
    api_key = os.environ.get("YT_API_KEY")
    if not api_key:
        raise ValueError("Please set the YT_API_KEY environment variable.")

    # Update channels with the latest statistics.
    update_channels(api_key, session)
