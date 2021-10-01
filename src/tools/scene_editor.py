# +++++ IMPORTS +++++
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import sys
import time

from src.misc.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT

class SceneEditor:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # Initialize shaders

        # Initialize model_matrix

        # Initialize view_matrix

        # Initialize projection_matrix

        self.clock = pygame.time.Clock()
        self.clock.tick()


    def update(self) -> None:
        delta_time = self.clock.tick() / 1000.0

        # Check key input

    def display(self) -> None:
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        # Draw things

        pygame.display.flip()

    def program_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit game")
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    pass

                elif event.type == pygame.KEYUP:
                    pass
        
            self.update()
            self.display()
        
        # Quit game
        self.quit()

    def start(self) -> None:
        self.program_loop()

    def quit(self) -> None:
        pygame.quit()

if __name__ == "__main__":
    SceneEditor().start()