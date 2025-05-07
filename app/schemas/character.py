from pydantic import BaseModel
from typing import List, Dict

class CharacterBase(BaseModel):
    character_name: str
    affiliation: str
    genetic_sequence: str
    power_level: int

class CharacterCreate(CharacterBase):
    pass

class PatternBase(BaseModel):
    pattern: str
    count: int

class Character(CharacterBase):
    id: int
    gc_content: float
    power_level_group: str
    patterns: List[PatternBase]

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    gc_content_by_character: Dict[str, float]
    common_patterns: List[Dict[str, int]]
    power_level_distribution: Dict[str, int]

class AffiliationStatsResponse(StatsResponse):
    pass 

class CharacterStatsResponse(CharacterBase):
    gc_content: float
    power_level_group: str
    patterns: List[PatternBase]
    id: int