# +++++ IMPORTS +++++
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import sys
import time
import math
from src.assets.types.walls import Walls
from src.misc.base_3d_objects import Cube

from src.misc.constants import *
from src.misc.point import Point
from src.misc.vector import Vector
from src.misc.shaders import Shader3D
from src.data.level_loader import LevelLoader
from src.misc.matrices import ModelMatrix, ProjectionMatrix, ViewMatrix

class Maze3D:
    def __init__(self, mode) -> None:
        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Lock mouse and keyboard to game window
        pygame.event.set_grab(True)

        # Load levels
        levelLoader = LevelLoader()
        levelLoader.read_level(LEVEL_1)
        self.levelGround = levelLoader.ground
        self.levelWalls = levelLoader.walls
        self.startPoint = levelLoader.startPoint
        self.endPoint = levelLoader.endPoint

        # Initialize shaders
        self.shader = Shader3D()
        self.shader.use()
        self.shader2 = Shader3D()
        self.shader2.use()

        # Initialize model_matrix
        self.modelMatrix = ModelMatrix()
        self.modelMatrix2 = ModelMatrix()

        # Initialize view_matrix
        self.viewMatrix = ViewMatrix()
        self.viewMatrix.look(Point(self.startPoint[0].position[0], self.startPoint[0].position[1], self.startPoint[0].position[2]), Point(0,0,0), Vector(0,1,0))
        self.shader.set_view_matrix(self.viewMatrix.get_matrix())
        self.viewMatrix2 = ViewMatrix()
        self.viewMatrix2.look(Point(self.startPoint[0].position[0], 40, self.startPoint[0].position[2]), Point(0,0,0), Vector(0,1,0))
        self.shader2.set_view_matrix(self.viewMatrix2.get_matrix())

        # Initialize projection_matrix
        self.projectionMatrix = ProjectionMatrix()
        self.projectionMatrix.set_perspective(math.pi/2, DISPLAY_WIDTH/DISPLAY_HEIGHT, 0.5, 100)
        self.shader.set_projection_matrix(self.projectionMatrix.get_matrix())
        self.projectionMatrix2 = ProjectionMatrix()
        self.projectionMatrix2.set_perspective(math.pi/2, DISPLAY_WIDTH/DISPLAY_HEIGHT, 0.5, 100)
        self.shader2.set_projection_matrix(self.projectionMatrix2.get_matrix())

        # Initialize cube object
        self.cube = Cube()
        self.cube2 = Cube()

        # Initialize clock
        self.clock = pygame.time.Clock()
        self.clock.tick()

        # Test variable
        self.angle = 0

        # Camera Mode
        self.cameraMode = mode
        self.topDownview = False
        self.thirdPersonView = False

        # Controls
        self.aIsPressed = False
        self.sIsPressed = False
        self.dIsPressed = False
        self.wIsPressed = False
        self.leftIsPressed = False
        self.downIsPressed = False
        self.rightIsPressed = False
        self.upIsPressed = False
        self.lShiftIsPressed = False

        # Mouse
        self.mouseMove = False

        # Collission 
        self.collission = False


    def update(self) -> None:
        # Set delta time
        delta_time = self.clock.tick() / 500.0
        # Breytti ur 1000.0 í 500.0

        self.angle += math.pi * delta_time
        if self.lShiftIsPressed:
            movementSpeed = MOVEMENTSPEED * 1.5
        else:
            movementSpeed = MOVEMENTSPEED

        # Movement disabled
        slidePosX = False
        slideNegX = False
        slidePosZ = False
        slideNegZ = False
        

        # Collision detection
        collisionRadius = 1
        for wall in self.levelWalls:
            data = wall.checkIfCollission(self.viewMatrix.eye.x, self.viewMatrix.eye.z, collisionRadius, self.viewMatrix.eye)
            # if data[0]: 
                # print(data)
                # print(self.viewMatrix.eye)
            if data[0]:
                self.collission = True
                if not slidePosX:
                    slidePosX = data[1]
                if not slideNegX:
                    slideNegX = data[2]
                if not slidePosZ:
                    slidePosZ = data[3]
                if not slideNegZ:
                    slideNegZ = data[4]


        # CHECK KEY INPUT
        # Keys: A, S, D, W
        jeff = [slidePosX, slideNegX, slidePosZ, slideNegZ]
        if self.cameraMode == EDIT_MODE:
            if self.aIsPressed:
                self.viewMatrix.slide(-movementSpeed * delta_time, 0, 0)
            if self.sIsPressed:
                self.viewMatrix.slide(0, 0, movementSpeed * delta_time)
            if self.dIsPressed:
                self.viewMatrix.slide(movementSpeed * delta_time, 0, 0)
            if self.wIsPressed:
                self.viewMatrix.slide(0, 0, -movementSpeed * delta_time)
        elif self.cameraMode == GAMER_MODE:
            if self.aIsPressed:
                self.viewMatrix.move(-movementSpeed * delta_time, 0, 0, jeff)
            if self.sIsPressed:
                self.viewMatrix.move(0, 0, movementSpeed * delta_time, jeff)
            if self.dIsPressed:
                self.viewMatrix.move(movementSpeed * delta_time, 0, 0, jeff)
            if self.wIsPressed:
                self.viewMatrix.move(0, 0, -movementSpeed * delta_time, jeff)

        if self.mouseMove:
            mouseXNew, mouseYNew = pygame.mouse.get_rel()
            mouseXNew = (mouseXNew / 25) * MOUSESENS
            mouseYNew = (mouseYNew / 25) * MOUSESENS
            if mouseXNew > 0:
                self.viewMatrix.yaw(-mouseXNew * delta_time)
            if mouseXNew < 0:
                self.viewMatrix.yaw(-mouseXNew * delta_time)
            if mouseYNew > 0:
                self.viewMatrix.pitch(-mouseYNew * delta_time)
            if mouseYNew < 0:
                self.viewMatrix.pitch(-mouseYNew * delta_time)

    def display(self) -> None:
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glViewport(0, DISPLAY_HEIGHT, 0, DISPLAY_WIDTH)
        #glClearColor(0.78, 1.0, 1.0, 1.0)

        # +++++ DRAW OBJECTS +++++
        self.shader.set_view_matrix(self.viewMatrix.get_matrix())

        self.modelMatrix.load_identity()

        self.cube.set_vertices(self.shader)

        for ground in self.levelGround:
            self.shader.set_solid_color(ground.color[0], ground.color[1], ground.color[2])
            self.modelMatrix.push_matrix()
            self.modelMatrix.add_translation(ground.translation[0], ground.translation[1], ground.translation[2])
            self.modelMatrix.add_rotate_x(ground.rotate[0])
            self.modelMatrix.add_rotate_y(ground.rotate[1])
            self.modelMatrix.add_rotate_z(ground.rotate[2])
            self.modelMatrix.add_scale(ground.scale[0], ground.scale[1], ground.scale[2])
            self.shader.set_model_matrix(self.modelMatrix.matrix)
            self.cube.draw(self.shader)
            self.modelMatrix.pop_matrix()

        # DRAW WALLS
        for wall in self.levelWalls:
            self.shader.set_solid_color(wall.color[0], wall.color[1], wall.color[2])
            self.modelMatrix.push_matrix()
            self.modelMatrix.add_translation(wall.translation[0], wall.translation[1], wall.translation[2])
            self.modelMatrix.add_rotate_x(wall.rotate[0])
            self.modelMatrix.add_rotate_y(wall.rotate[1])
            self.modelMatrix.add_rotate_z(wall.rotate[2])
            self.modelMatrix.add_scale(wall.scale[0], wall.scale[1], wall.scale[2])
            self.shader.set_model_matrix(self.modelMatrix.matrix)
            self.cube.draw(self.shader)
            self.modelMatrix.pop_matrix()
        
        if self.topDownview or self.thirdPersonView:
            self.shader.set_solid_color(1, 0, 0)
            self.modelMatrix.push_matrix()
            self.modelMatrix.add_translation(self.viewMatrix.eye.x, 0.0, self.viewMatrix.eye.z)
            self.modelMatrix.add_scale(1, 2, 1)
            self.shader.set_model_matrix(self.modelMatrix.matrix)
            self.cube.draw(self.shader)
            self.modelMatrix.pop_matrix()

        pygame.display.flip()

    def display2(self) -> None:
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #glViewport(720, 0, 720, 450)
        #pygame.display.set_mode(720, 0, 720, 450)
        #glClearColor(0.78, 1.0, 1.0, 1.0)

        # +++++ DRAW OBJECTS +++++
        self.shader.set_view_matrix(self.viewMatrix.get_matrix())

        self.modelMatrix.load_identity()

        self.cube.set_vertices(self.shader2)

        for ground in self.levelGround:
            self.shader.set_solid_color(ground.color[0], ground.color[1], ground.color[2])
            self.modelMatrix.push_matrix()
            self.modelMatrix.add_translation(ground.translation[0], ground.translation[1], ground.translation[2])
            self.modelMatrix.add_rotate_x(ground.rotate[0])
            self.modelMatrix.add_rotate_y(ground.rotate[1])
            self.modelMatrix.add_rotate_z(ground.rotate[2])
            self.modelMatrix.add_scale(ground.scale[0], ground.scale[1], ground.scale[2])
            self.shader.set_model_matrix(self.modelMatrix.matrix)
            self.cube.draw(self.shader)
            self.modelMatrix.pop_matrix()

        # DRAW WALLS
        for wall in self.levelWalls:
            self.shader.set_solid_color(wall.color[0], wall.color[1], wall.color[2])
            self.modelMatrix.push_matrix()
            self.modelMatrix.add_translation(wall.translation[0], wall.translation[1], wall.translation[2])
            self.modelMatrix.add_rotate_x(wall.rotate[0])
            self.modelMatrix.add_rotate_y(wall.rotate[1])
            self.modelMatrix.add_rotate_z(wall.rotate[2])
            self.modelMatrix.add_scale(wall.scale[0], wall.scale[1], wall.scale[2])
            self.shader.set_model_matrix(self.modelMatrix.matrix)
            self.cube.draw(self.shader)
            self.modelMatrix.pop_matrix()
        
        self.shader.set_solid_color(1, 0, 0)
        self.modelMatrix.push_matrix()
        self.modelMatrix.add_translation(self.viewMatrix.eye.x, 0.0, self.viewMatrix.eye.z)
        self.modelMatrix.add_scale(1, 2, 1)
        self.shader.set_model_matrix(self.modelMatrix.matrix)
        self.cube.draw(self.shader)
        self.modelMatrix.pop_matrix()

    def program_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit game")
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # Danni code
                    # Esc key to quit game
                    if event.key == K_ESCAPE:
                        print("Quit game")
                        running = False
                    # Keys: A, S, D, W
                    elif event.key == K_a:
                        self.aIsPressed = True
                    elif event.key == K_s:
                        self.sIsPressed = True
                    elif event.key == K_d:
                        self.dIsPressed = True
                    elif event.key == K_w:
                        self.wIsPressed = True
                    # Keys: Left, Down, Right, Up
                    elif event.key == K_LEFT:
                        self.leftIsPressed = True
                    elif event.key == K_DOWN:
                        self.downIsPressed = True
                    elif event.key == K_RIGHT:
                        self.rightIsPressed = True
                    elif event.key == K_UP:
                        self.upIsPressed = True
                    # Key: Left Shift
                    elif event.key == K_LSHIFT:
                        self.lShiftIsPressed = True
                    # Key: T
                    elif event.key == K_r:
                        self.thirdPersonView = True
                        self.viewMatrix.viewMode = 1
                    # Key: T
                    elif event.key == K_t:
                        self.topDownview = True
                        self.viewMatrix.viewMode = 2
                    
                
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
                    # Keys: Left, Down, Right, Up
                    elif event.key == K_LEFT:
                        self.leftIsPressed = False
                    elif event.key == K_DOWN:
                        self.downIsPressed = False
                    elif event.key == K_RIGHT:
                        self.rightIsPressed = False
                    elif event.key == K_UP:
                        self.upIsPressed = False
                    # Key: Left Shift
                    elif event.key == K_LSHIFT:
                        self.lShiftIsPressed = False
                    # Key: T
                    elif event.key == K_r:
                        self.thirdPersonView = False
                        self.viewMatrix.viewMode = 1
                    # Key: T
                    elif event.key == K_t:
                        self.topDownview = False
                        self.viewMatrix.viewMode = 0
                
                elif event.type == pygame.MOUSEMOTION:
                    self.mouseMove = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                elif event.type == pygame.MOUSEBUTTONUP:
                    pass

                else:
                    self.mouseMove = False

        
            self.update()
            self.display()
            self.display2()
        
        # Quit game
        self.quit()

    def start(self) -> None:
        self.program_loop()

    def quit(self) -> None:
        pygame.quit()

if __name__ == "__main__":
    Maze3D().start()