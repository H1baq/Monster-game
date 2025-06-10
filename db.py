from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///monster_game.db')
Session = sessionmaker(bind=engine)
