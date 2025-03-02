import asyncio
from prisma import Prisma


# Enum for political parties
class Party:
    CDU = "CDU"
    SPD = "SPD"
    FDP = "FDP"
    GRUENE = "GRUENE"
    LINKE = "LINKE"
    AFD = "AFD"


# Initialize Prisma Client
db = Prisma()


async def seed_parties():
    """Seeds the database with predefined political parties."""
    german_parties = [
        {"id": 1, "name": "CDU"},
        {"id": 2, "name": "SPD"},
        {"id": 3, "name": "FDP"},
        {"id": 4, "name": "Bündnis 90/Die Grünen"},
        {"id": 5, "name": "Die Linke"},
        {"id": 6, "name": "AfD"},
    ]

    await db.party.create_many(
        data=german_parties,
        skip_duplicates=True,  # Avoids duplicate insertion
    )


async def seed_channel(name: str, channel_id: str, party_id: int, is_party_channel: bool = False):
    """Seeds the database with YouTube channels."""
    try:
        channel = await db.channel.create(
            data={
                "name": name,
                "channel_id": channel_id,
                "partyId": party_id,  # Ensure ID exists in Party
                "is_party_channel": is_party_channel,
            }
        )
        print(f"✅ Seeded channel: {channel}")
    except Exception as error:
        print(f"❌ Error seeding channel: {error}")


async def main():
    await db.connect()

    # Clear existing entries (optional)
    await db.channel_update.delete_many()
    await db.channel.delete_many()
    await db.party.delete_many()

    # Seed parties
    await seed_parties()

    # Retrieve party IDs from database
    parties = await db.party.find_many()
    party_id_map = {party.name: party.id for party in parties}

    # Seed channels
    await seed_channel("CDU", "UCKyWIEse3u7ExKfAWuDMVnw", party_id_map.get("CDU"), True)
    await seed_channel("SPD", "UCSmbK1WtpYn2sOGLvSSXkKw", party_id_map.get("SPD"), True)
    await seed_channel("FDP", "UC-sMkrfoQDH-xzMxPNckGFw", party_id_map.get("FDP"), True)
    await seed_channel("Bündnis 90/Die Grünen", "UC7TAA2WYlPfb6eDJCeX4u0w", party_id_map.get("Bündnis 90/Die Grünen"), True)
    await seed_channel("Die Linke", "UCA95T5bSGxNOAODBdbR2rYQ", party_id_map.get("Die Linke"), True)
    await seed_channel("AFD", "UCq2rogaxLtQFrYG3X3KYNww", party_id_map.get("AfD"), True)
    await seed_channel("Ketzer der Neuzeit", "UCjvVn-oLzoY0aZhVvdQPSTQ", party_id_map.get("AfD"))

    print("🎉 Seeding completed successfully.")
    await db.disconnect()


# Run the seeding script
if __name__ == "__main__":
    asyncio.run(main())
