

from typing import Dict


class Character:
    
    def __init__(self, name: str):
        self.name = name
        self.relationships: Dict[Character, float] = {}
        
    