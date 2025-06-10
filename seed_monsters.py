from db import Session
from models.base import Base
from models.monster_species import MonsterSpecies
from sqlalchemy import create_engine

engine = create_engine("sqlite:///monster_game.db")
Base.metadata.create_all(engine)

session = Session()

monster_data = [
    {"name": "Flamewyrm", "type": "Fire", "base_stats": {"hp": 45, "attack": 60, "defense": 40, "speed": 50}, "rarity": "Common", "abilities": ["Fire Blast", "Tail Whip"]},
    {"name": "Aquafin", "type": "Water", "base_stats": {"hp": 50, "attack": 45, "defense": 55, "speed": 40}, "rarity": "Common", "abilities": ["Aqua Heal", "Bubble"]},
    {"name": "Vinewhip", "type": "Grass", "base_stats": {"hp": 55, "attack": 40, "defense": 50, "speed": 45}, "rarity": "Common", "abilities": ["Vine Lash", "Grow"]},
    {"name": "Sparkbolt", "type": "Electric", "base_stats": {"hp": 35, "attack": 65, "defense": 30, "speed": 70}, "rarity": "Rare", "abilities": ["Thunder Shock", "Charge"]},
    {"name": "Rockgrinder", "type": "Earth", "base_stats": {"hp": 70, "attack": 50, "defense": 70, "speed": 25}, "rarity": "Uncommon", "abilities": ["Mud Slap", "Rock Throw"]},
    {"name": "Breezette", "type": "Air", "base_stats": {"hp": 40, "attack": 35, "defense": 40, "speed": 80}, "rarity": "Uncommon", "abilities": ["Gust", "Whirlwind"]},
    {"name": "Infernox", "type": "Fire", "base_stats": {"hp": 65, "attack": 85, "defense": 60, "speed": 70}, "rarity": "Rare", "abilities": ["Inferno", "Scorch"]},
    {"name": "Hydrake", "type": "Water", "base_stats": {"hp": 60, "attack": 70, "defense": 65, "speed": 60}, "rarity": "Uncommon", "abilities": ["Water Jet", "Soak"]},
    {"name": "Leaflurker", "type": "Grass", "base_stats": {"hp": 50, "attack": 55, "defense": 60, "speed": 55}, "rarity": "Common", "abilities": ["Leaf Blade", "Camouflage"]},
    {"name": "Voltar", "type": "Electric", "base_stats": {"hp": 40, "attack": 60, "defense": 35, "speed": 80}, "rarity": "Rare", "abilities": ["Shock Wave", "Paralyze"]},
    {"name": "Quakejaw", "type": "Earth", "base_stats": {"hp": 75, "attack": 80, "defense": 85, "speed": 30}, "rarity": "Rare", "abilities": ["Earthquake", "Sandstorm"]},
    {"name": "Whispry", "type": "Air", "base_stats": {"hp": 45, "attack": 40, "defense": 45, "speed": 90}, "rarity": "Common", "abilities": ["Air Slash", "Tailwind"]},
    {"name": "Embercub", "type": "Fire", "base_stats": {"hp": 50, "attack": 55, "defense": 35, "speed": 45}, "rarity": "Common", "abilities": ["Ember", "Growl"]},
    {"name": "Torrento", "type": "Water", "base_stats": {"hp": 65, "attack": 70, "defense": 55, "speed": 50}, "rarity": "Legendary", "abilities": ["Tsunami", "Bubble Beam"]},
    {"name": "Stormling", "type": "Electric", "base_stats": {"hp": 55, "attack": 75, "defense": 40, "speed": 85}, "rarity": "Legendary", "abilities": ["Lightning Strike", "Discharge"]},
]

species_objects = [MonsterSpecies(**data) for data in monster_data]
session.bulk_save_objects(species_objects)
session.commit()
