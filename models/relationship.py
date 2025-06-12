from sqlalchemy import Column, Integer, Enum, ForeignKey
from models.base import Base

class Relationship(Base):
    __tablename__ = 'relationships'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    target_player_id = Column(Integer, ForeignKey('players.id'))
    relation_type = Column(Enum("friend", "rival", name="relation_type_enum"), nullable=False)
