from pydantic import BaseModel
from typing import Dict, List

class StatsResponse(BaseModel):
    total_characters: int
    average_power_level: float
    power_level_groups: Dict[str, int]
    average_gc_content: float
    top_affiliations: List[Dict[str, int]]
    visualizations: Dict[str, str] 