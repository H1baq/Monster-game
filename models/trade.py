from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from models.base  import Base

class Trade(Base):
    __tablename__ = 'trade'

    id=Column(Integer, primary_key=True)
    sender_id=Column(Integer, ForeignKey('players.id'))
    receiver_id = Column(Integer, ForeignKey('players.id'))
    offered_monster_id = Column(Integer, ForeignKey('player_monsters.id'))
    requested_monster_id = Column(Integer, ForeignKey('player_monsters.id'))
    status = Column(Enum("pending", "accepted", "declined", name="trade_status"), default="pending")
