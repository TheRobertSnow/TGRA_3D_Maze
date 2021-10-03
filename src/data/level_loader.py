import json
import sys

from src.assets.types.walls import Walls
from src.assets.types.ground import Ground

class LevelLoader:
    # Should load in levels from 'src/data/levels' into
    # appropriate class in 'src/assets/types'
    def __init__(self) -> None:
        self.fPrefix = sys.path[0] + "/src/data/levels/"

        self.walls = []
        self.ground = []

    def read_level(self, fileName):
        f = open(self.fPrefix+fileName, 'r')
        data = json.loads(f.read())
        
        # Load walls
        for i in data["walls"]:
            wall = Walls(i["color3f"], i["translation3f"], i["rotate3f"], i["scale3f"])
            self.walls.append(wall)

        # Load ground
        for i in data["ground"]:
            ground = Ground(i["color3f"], i["translation3f"], i["rotate3f"], i["scale3f"])
            self.ground.append(ground)
        


if __name__ == "__main__":
    LevelLoader().read_level("level1.json")