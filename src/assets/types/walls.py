
class Walls:
    # Class for handeling walls
    def __init__(self, color, translation, rotate, scale) -> None:
        self.color = color
        self.translation = translation
        self.rotate = rotate
        self.scale = scale

    def checkIfCollission(self, x, z):
        if x > self.translation[0] - (self.scale[0] * 0.5) and x < self.translation[0] + (self.scale[0] * 0.5) and z > self.translation[2] - (self.scale[2] * 0.5) and z < self.translation[2] + (self.scale[2] * 0.5):
            return True
        else:
            return False