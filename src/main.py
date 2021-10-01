# +++++ IMPORTS +++++
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import sys
import time
import math
from src.misc.base_3d_objects import Cube

from src.misc.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from src.misc.point import Point
from src.misc.vector import Vector
from src.misc.shaders import Shader3D
from src.misc.matrices import ModelMatrix, ProjectionMatrix, ViewMatrix

class Maze3D:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Initialize shaders
        self.shader = Shader3D()
        self.shader.use()

        # Initialize model_matrix
        self.modelMatrix = ModelMatrix()

        # Initialize view_matrix
        self.viewMatrix = ViewMatrix()
        self.viewMatrix.look(Point(3,3,3), Point(0,0,0), Vector(0,1,0))
        self.shader.set_view_matrix(self.viewMatrix.get_matrix())

        # Initialize projection_matrix
        self.projectionMatrix = ProjectionMatrix()
        self.projectionMatrix.set_perspective(math.pi/2, DISPLAY_WIDTH/DISPLAY_HEIGHT, 0.5, 100)
        self.shader.set_projection_matrix(self.projectionMatrix.get_matrix())

        # Initialize cube object
        self.cube = Cube()

        # Initialize clock
        self.clock = pygame.time.Clock()
        self.clock.tick()

        # Test variable
        self.angle = 0

        # Controls
        self.aIsPressed = False
        self.sIsPressed = False
        self.dIsPressed = False
        self.wIsPressed = False
        self.upIsPressed = False
        self.downIsPressed = False


    def update(self) -> None:
        # Set delta time
        delta_time = self.clock.tick() / 1000.0

        self.angle += math.pi * delta_time
        
        # CHECK KEY INPUT
        # Keys: A, S, D, W
        if self.aIsPressed:
            self.viewMatrix.slide(-1 * delta_time, 0, 0)
        if self.sIsPressed:
            self.viewMatrix.slide(0, 0, 1 * delta_time)
        if self.dIsPressed:
            self.viewMatrix.slide(1 * delta_time, 0, 0)
        if self.wIsPressed:
            self.viewMatrix.slide(0, 0, -1 * delta_time)
        
        # Keys: Arrow Up, Arrow Down
        if self.upIsPressed:
            self.viewMatrix.roll(math.pi * delta_time)
        if self.downIsPressed:
            self.viewMatrix.roll(-math.pi * delta_time)
    

    def display(self) -> None:
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        # +++++ DRAW OBJECTS +++++
        self.shader.set_view_matrix(self.viewMatrix.get_matrix())

        self.modelMatrix.load_identity()

        self.cube.set_vertices(self.shader)

        self.shader.set_solid_color(0.0, 1.0, 1.0)
        self.modelMatrix.push_matrix()
        self.modelMatrix.add_translation(0.0, 2.5, 0.0)
        self.modelMatrix.add_rotate_z(self.angle)
        self.modelMatrix.add_rotate_x(self.angle)
        self.modelMatrix.add_scale(1.0, 1.0, 2.0)
        self.shader.set_model_matrix(self.modelMatrix.matrix)
        self.cube.draw(self.shader)
        self.modelMatrix.pop_matrix()

        self.shader.set_solid_color(1.0, 1.0, 0.0)
        self.modelMatrix.push_matrix()
        self.modelMatrix.add_translation(0.0, 0.0, 2.0)
        self.modelMatrix.add_rotate_y(self.angle)
        self.modelMatrix.add_scale(2.0, 1.0, 1.0)
        self.shader.set_model_matrix(self.modelMatrix.matrix)
        self.cube.draw(self.shader)
        self.modelMatrix.pop_matrix()

        self.shader.set_solid_color(1.0, 0.0, 1.0)
        self.modelMatrix.push_matrix()
        self.modelMatrix.add_translation(0.0, 0.0, 0.0)
        self.shader.set_model_matrix(self.modelMatrix.matrix)
        self.cube.draw(self.shader)
        self.modelMatrix.pop_matrix()
        # +++++ END DRAW +++++

        pygame.display.flip()

    def program_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit game")
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # Keys: A, S, D, W
                    if event.key == K_a:
                        self.aIsPressed = True
                    elif event.key == K_s:
                        self.sIsPressed = True
                    elif event.key == K_d:
                        self.dIsPressed = True
                    elif event.key == K_w:
                        self.wIsPressed = True
                    # Keys: Arrow Up, Arrow Down
                    elif event.key == K_UP:
                        self.upIsPressed = True
                    elif event.key == K_DOWN:
                        self.downIsPressed = True
                    
                
                elif event.type == pygame.KEYUP:
                    # Keys: A, S, D, W
                    if event.key == K_a:
                        self.aIsPressed = False
                    elif event.key == K_s:
                        self.sIsPressed = False
                    elif event.key == K_d:
                        self.dIsPressed = False
                    elif event.key == K_w:
                        self.wIsPressed = False
                    # Keys: Arrow Up, Arrow Down
                    elif event.key == K_UP:
                        self.upIsPressed = False
                    elif event.key == K_DOWN:
                        self.downIsPressed = False
                
                elif event.type == pygame.MOUSEMOTION:
                    pass

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                elif event.type == pygame.MOUSEBUTTONUP:
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
    Maze3D().start()