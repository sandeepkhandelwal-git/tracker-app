from sqlalchemy import Column, Integer, Float, DateTime, func, String
from app.database.session import Base

class UserLocation(Base):
    __tablename__ = 'user_locations'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True),server_default=func.now())
