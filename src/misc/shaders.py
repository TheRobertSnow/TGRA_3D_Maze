
from OpenGL.GL import *
from math import * # trigonometry

import sys

from src.misc.base_3d_objects import *
from src.misc.constants import SIMPLE_3D_VERT, SIMPLE_3D_FRAG

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + SIMPLE_3D_VERT)
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + SIMPLE_3D_FRAG)
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc              = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)


        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.ViewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc    = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        # self.colorLoc               =glGetUniformLocation(self.renderingProgramID, "u_color")
        self.eyePositionLoc               =glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        self.directionalLightLoc        =glGetUniformLocation(self.renderingProgramID, "u_directional_light")

        self.numberOfLightsLoc              =glGetUniformLocation(self.renderingProgramID, "u_number_of_lights")
        self.lightPositionLoc               =glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffuseLoc               =glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecularLoc               =glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        
        self.materialDiffuseLoc               =glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc               =glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialAmbientLoc                 =glGetUniformLocation(self.renderingProgramID, "u_mat_ambient")
        self.materialShininessLoc               =glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.ViewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)
    
    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    # def set_solid_color(self, r, g, b):
    #     glUniform4f(self.colorLoc, r, g, b, 1.0)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePositionLoc, pos.x, pos.y, pos.z, 1.0)

    def set_directional_light(self, r, g, b):
        glUniform4f(self.directionalLightLoc, r, g, b, 1.0)

    def set_number_of_lights(self, value): 
        glUniform1i(self.numberOfLightsLoc, value)

    # def set_light_position(self, pos):
    #     glUniform4f(self.lightPositionLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos):
        glUniform4fv(self.lightPositionLoc, len(pos), pos)
    
    # def set_light_diffuse(self, point):
    #     glUniform4f(self.lightDiffuseLoc, point.r, point.g, point.b, 1.0)

    def set_light_diffuse(self, diff):
        glUniform4fv(self.lightDiffuseLoc, len(diff), diff)
    
    # def set_light_specular(self, point):
    #     glUniform4f(self.lightSpecularLoc, point.r, point.g, point.b, 1.0)

    def set_light_specular(self, spec):
        glUniform4fv(self.lightSpecularLoc, len(spec), spec)
    
    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.materialDiffuseLoc, r, g, b, 1.0)
    
    def set_material_specular(self, r, g, b):
        glUniform4f(self.materialSpecularLoc, r, g, b, 1.0)
    
    def set_material_ambient(self, r, g, b):
        glUniform4f(self.materialAmbientLoc, r, g, b, 1.0)
    
    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)

