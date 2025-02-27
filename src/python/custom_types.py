import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

# SQLAlchemy base class
Base = declarative_base()


# Define the Party model
class Party(Base):
    __tablename__ = 'Party'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)


# Define the Channel model
class Channel(Base):
    __tablename__ = 'Channel'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)
    is_party_channel = Column(Boolean, default=False)
    partyId = Column(BigInteger, ForeignKey('Party.id', ondelete="CASCADE"), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)


# Define the Channel_Update model
class Channel_Update(Base):
    __tablename__ = 'Channel_Update'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    channelId = Column("channel_Id", String, ForeignKey('Channel.id', ondelete="CASCADE"), nullable=False)
    subscriber = Column(BigInteger, default=0, nullable=True)
    views = Column(BigInteger, default=0, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)


# Define the Youtube_Video model
class Youtube_Video(Base):
    __tablename__ = 'Youtube_Video'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    channelId = Column(String, ForeignKey('Channel.id', ondelete="CASCADE"), nullable=False)
    transcript = Column(String, nullable=False)
    video_id = Column(String, unique=True, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)


# Define the Youtube_Video_Update model
class Youtube_Video_Update(Base):
    __tablename__ = 'Youtube_Video_Update'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    youtube_VideoId = Column(String, ForeignKey('Youtube_Video.id', ondelete="CASCADE"), nullable=False)
    views = Column(BigInteger, default=0, nullable=False)
    likes = Column(BigInteger, default=0, nullable=False)
    comment_amount = Column(BigInteger, default=0, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
