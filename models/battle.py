from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    monster_id = Column(Integer, ForeignKey("player_monsters.id"))
    opponent = Column(String)
    won = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("Player", back_populates="battles")
    monster = relationship("PlayerMonster", back_populates="battles")
