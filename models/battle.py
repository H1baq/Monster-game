from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Battle(Base):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey('players.id'))
    player2_id = Column(Integer, ForeignKey('players.id'))
    winner_id = Column(Integer, ForeignKey('players.id'), nullable=True)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    player_1 = relationship("Player", foreign_keys=[player1_id], back_populates="battles_as_player_1")
    player_2 = relationship("Player", foreign_keys=[player2_id], back_populates="battles_as_player_2")
    winner = relationship("Player", foreign_keys=[winner_id])

    monster_battles = relationship("MonsterBattle", back_populates="battle", cascade="all, delete")
