from os import DirEntry
from src.misc.vector import Vector

class EvilObject:
    # Class for handeling walls
    def __init__(self, color, translationStart, translationEnd, rotate, scale) -> None:
        self.color = color
        self.translationStart = translationStart
        self.translationEnd = translationEnd
        self.translationCurr = Vector(self.translationStart[0], self.translationStart[1], self.translationStart[2])
        self.rotate = rotate
        self.scale = scale
        self.direction = Vector(self.translationStart[0], self.translationStart[1], self.translationStart[2]) - Vector(self.translationEnd[0], self.translationEnd[1], self.translationEnd[2])

    def update(self, move):
        if self.direction.x != 0:
            if self.direction.x > 0:
                self.translationCurr.x -= move
                if self.translationCurr.x < self.translationStart[0]:
                    self.direction.x = -self.direction.x
            elif self.direction.x < 0:
                self.translationCurr.x += move
                if self.translationCurr.x > self.translationEnd[0]:
                    self.direction.x = -self.direction.x
        if self.direction.z != 0:
            if self.direction.z > 0:
                self.translationCurr.z -= move
                if self.translationCurr.z < self.translationStart[2]:
                    self.direction.z = -self.direction.z
            elif self.direction.z < 0:
                self.translationCurr.z += move
                if self.translationCurr.z > self.translationEnd[2]:
                    self.direction.z = -self.direction.z
