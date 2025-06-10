from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class PlayerMonster(Base):
    __tablename__ = 'player_monsters'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    species_id = Column(Integer, ForeignKey('monster_species.id'), nullable=False)

    nickname = Column(String, default=None)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    stats = Column(JSON)  # individual stats based on species base stats + level
    date_caught = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies")

    def __repr__(self):
        return f"<PlayerMonster {self.nickname or self.species.name} (Lv. {self.level})>"
