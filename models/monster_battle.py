from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class MonsterBattle(Base):
    __tablename__ = 'monster_battles'

    id = Column(Integer, primary_key=True)
    battle_id = Column(Integer, ForeignKey('battles.id'))
    player_monster_id = Column(Integer, ForeignKey('player_monsters.id'))

    battle = relationship("Battle", back_populates="monster_battles")
    player_monster = relationship("PlayerMonster", back_populates="monster_battles")
