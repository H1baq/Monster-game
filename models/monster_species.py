# import necessary modules for the MonsterSpecies model
#JSON is used to store complex data structures like abilities and base stats
from sqlalchemy import Column, Integer, String, JSON
from models.base import Base

# This file defines the MonsterSpecies model, which represents different species of monsters in the game.
# It includes attributes such as name, type, base stats, rarity, and abilities.
class MonsterSpecies(Base):
    __tablename__ = 'monster_species'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(String)  # Fire, Water, etc.
    base_stats = Column(JSON)  # {"hp": 45, "attack": 60, "defense": 40, "speed": 50}
    rarity = Column(String)  # Common, Uncommon, Rare, Legendary
    abilities = Column(JSON)  # ["Fire Blast", "Tail Whip"]

    
