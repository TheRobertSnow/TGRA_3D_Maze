from src.main import Maze3D
from src.misc.constants import GAMER_MODE, MODES
import sys, getopt

if __name__ == "__main__":
    mode = GAMER_MODE
    argv = sys.argv
    if len(argv) > 1:
        if argv[1] == '-m':
            if argv[2] in MODES:
                mode = argv[2]
    Maze3D(mode).start()