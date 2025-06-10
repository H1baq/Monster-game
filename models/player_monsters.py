# import necessary modules
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

# This file defines the PlayerMonster model, which represents a player's monster in the game.
# It includes attributes such as player ID, species ID, level, current HP, and nickname.
class PlayerMonster(Base):
    __tablename__ = 'player_monsters'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    species_id = Column(Integer, ForeignKey('monster_species.id'))
    level = Column(Integer, default=1)
    current_hp = Column(Integer)
    nickname = Column(String)

    # Relationships between PlayerMonster and other models
    player = relationship("Player", backref="monsters")
    species = relationship("MonsterSpecies", backref="instances")
