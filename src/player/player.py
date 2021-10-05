
from src.misc.point import Point


class Player:
    def __init__(self, startPoint: Point) -> None:
        self.position = startPoint
    
    def update(self) -> None:
        """Update the player position"""
        pass
    
    def display(self) -> None:
        """Draw the player"""
        pass

    def __str__(self) -> str:
        pass