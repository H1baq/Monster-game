# import necessary modules
from sqlalchemy import Column, Integer, String, ForeignKey
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
    experience = Column(Integer, default=0)

    def gain_experience(self, amount):
            """Add EXP and level up if threshold is reached."""
            self.experience += amount
            exp_to_level = self.level * 100

            leveled_up = False
            while self.experience >= exp_to_level:
                self.experience -= exp_to_level
                self.level += 1
                leveled_up = True
                exp_to_level = self.level * 100

            return leveled_up


    # Relationships between PlayerMonster and other models
    player = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", backref="instances")
