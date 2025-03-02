import asyncio
import os
from dotenv import load_dotenv
from prisma import Prisma
from googleapiclient.discovery import build


async def get_channel_statistics(api_key: str, channel_id: str) -> dict:
    """
    Fetches YouTube channel statistics via YouTube API.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(part='statistics', id=channel_id)
    response = request.execute()
    return response


async def update_channels(api_key: str, db: Prisma):
    """
    Retrieves all channels from the database, fetches their statistics,
    and updates the Channel_Update table with new data.
    """
    channels = await db.channel.find_many()

    for channel in channels:
        stats = await get_channel_statistics(api_key, channel.channel_id)

        if 'items' in stats and stats['items']:
            statistics = stats['items'][0].get('statistics', {})
            subscriber_count = int(statistics.get('subscriberCount', 0))
            view_count = int(statistics.get('viewCount', 0))

            print(f"Updating channel {channel.name}: Subscribers={subscriber_count}, Views={view_count}")

            # Create a new Channel_Update record
            await db.channel_update.create(
                data={
                    "channel_Id": str(channel.id),  # ✅ Ensure correct field name & convert to string
                    "subscriber": subscriber_count,
                    "views": view_count
                }
            )
        else:
            print(f"No statistics found for channel ID: {channel.channel_id}")


async def main():
    load_dotenv(dotenv_path="./.env")

    YT_API_KEY = os.getenv("YT_API_KEY")

    if not YT_API_KEY:
        raise ValueError("Please set the YT_API_KEY environment variable.")

    # Connect to Prisma database
    db = Prisma()
    await db.connect()

    # Update YouTube channel stats
    await update_channels(YT_API_KEY, db)

    await db.disconnect()
    print("✅ Channel statistics updated successfully.")


if __name__ == "__main__":
    asyncio.run(main())
