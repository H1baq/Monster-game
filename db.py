from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.player import Player
from models.monster_species import MonsterSpecies
from models.player_monsters import PlayerMonster
from models.battle import Battle

engine = create_engine('sqlite:///monster_game.db')
Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
    
if __name__ == "__main__":
    create_tables()

