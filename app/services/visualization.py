import os
import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive Agg
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.character import Character
from app.utils.logger import logger

class VisualizationService:
    def __init__(self):
        self.static_dir = "static/graphs"
        os.makedirs(self.static_dir, exist_ok=True)

    def generate_power_level_distribution(self, characters: List[Character]) -> str:
        """Generate and save power level distribution graph."""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=[c.power_level for c in characters], bins=20)
        plt.title("Power Level Distribution")
        plt.xlabel("Power Level")
        plt.ylabel("Count")
        
        filename = "power_level_distribution.png"
        filepath = os.path.join(self.static_dir, filename)
        plt.savefig(filepath)
        plt.close()
        
        return f"/static/graphs/{filename}"

    def generate_gc_content_distribution(self, characters: List[Character]) -> str:
        """Generate and save GC content distribution graph."""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=[c.gc_content for c in characters], bins=20)
        plt.title("GC Content Distribution")
        plt.xlabel("GC Content (%)")
        plt.ylabel("Count")
        
        filename = "gc_content_distribution.png"
        filepath = os.path.join(self.static_dir, filename)
        plt.savefig(filepath)
        plt.close()
        
        return f"/static/graphs/{filename}"

    def generate_affiliation_pie_chart(self, characters: List[Character]) -> str:
        """Generate and save affiliation distribution pie chart."""
        plt.figure(figsize=(10, 6))
        affiliation_counts = {}
        for char in characters:
            affiliation_counts[char.affiliation] = affiliation_counts.get(char.affiliation, 0) + 1
        
        plt.pie(affiliation_counts.values(), labels=affiliation_counts.keys(), autopct='%1.1f%%')
        plt.title("Character Affiliation Distribution")
        
        filename = "affiliation_distribution.png"
        filepath = os.path.join(self.static_dir, filename)
        plt.savefig(filepath)
        plt.close()
        
        return f"/static/graphs/{filename}"

visualization_service = VisualizationService() 