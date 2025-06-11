from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base import Base

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    experience = Column(Float, default=0, nullable=False)
    money = Column(Float, default=0, nullable=False)

    monsters = relationship("PlayerMonster", back_populates="player", cascade="all, delete-orphan")

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

    def __repr__(self):
        return f"<Player(id={self.id}, username='{self.username}', level={self.level}, xp={self.experience})>"
