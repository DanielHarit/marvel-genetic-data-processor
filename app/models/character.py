from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String, index=True)
    affiliation = Column(String, index=True)
    genetic_sequence = Column(String)
    power_level = Column(Integer)
    gc_content = Column(Float)
    power_level_group = Column(String)

    patterns = relationship("Pattern", back_populates="character")

class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    pattern = Column(String, index=True)
    count = Column(Integer)

    character = relationship("Character", back_populates="patterns") 