
class Walls:
    # Class for handeling walls
    def __init__(self, color, translation, rotate, scale) -> None:
        self.color = color
        self.translation = translation
        self.rotate = rotate
        self.scale = scale

    def checkIfCollission(self, x, z, r, eye):
        # Return list:
        # [bool, bool, bool, bool, bool]
        # [Collision detected, disable +x, disable -x, disable +z, disable -z]
        P1_x = self.translation[0] - (self.scale[0] * 0.5)
        P1_z = self.translation[2] - (self.scale[2] * 0.5)
        P2_x = self.translation[0] + (self.scale[0] * 0.5)
        P2_z = self.translation[2] + (self.scale[2] * 0.5)
        if x+r >= P1_x \
        and z+r >= P1_z \
        and x-r <= P2_x \
        and z-r <= P2_z:
            # Check if above or below
            if eye.x >= P1_x and eye.x <= P2_x:
                if eye.z < P1_z: # Below wall
                    # Disable move +z
                    return [True, False, False, True, False]
                elif eye.z > P2_z: # Above wall
                    # Disable move -z
                    return [True, False, False, False, True]
                else:
                    return [False, False, False, False, False]
            # Check if left or right
            if eye.z >= P1_z and eye.z <= P2_z:
                if eye.x < P1_x: # Left of wall
                    # Disable move +x
                    return [True, True, False, False, False]
                elif eye.x > P2_x: # Right of wall
                    # Disable move -x
                    return [True, False, True, False, False]
                else:
                    return [False, False, False, False, False]
            else:
                return [False, False, False, False, False]
        else:
            return [False, False, False, False, False]