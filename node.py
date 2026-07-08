import random
from OpenGL.GL import glCallList, glColor3f, glMaterialfv, glMultMatrixf, glPopMatrix, glPushMatrix, \
                      GL_EMISSION, GL_FRONT
import numpy

from primitive import G_OBJ_CUBE, G_OBJ_SPHERE
from aabb import AABB
from transformation import scaling, translation
import color

class Node(object):
    """Our "Primitive" """
    def __init__(self):
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5,0.5, 0.5])
        self.translation_matrix = numpy.identity(4)
        self.scaling_matrix = numpy.identity(4)
        self.selected = False

    def render(self):
        """Render the item to our screen"""
        glPushMatrix()
        glMultMatrixf(numpy.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        cur_color = color.COLORS[self.color_index]
        glColor3f(cur_color[0], cur_color[1], cur_color[2])
        if self.selected: #If node is selected glow
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])
        self.render_self()

        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])
        glPopMatrix()

    def render_self(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'render_self'"
        )
    def pick(self, start, direction, mat):

        newmat = numpy.dot(
            numpy.dot(mat, self.translation_matrix),
            numpy.linalg.inv(self.scaling_matrix)
        )
        results = self.aabb.ray_hit(start, direction, newmat)
        return results
    
    def select(self, select=None):
        if select is not None:
            self.selected = select

        else:
            self.selected = not self.selected

    def rotate_color(self, forwards):
        self.color_index += 1 if forwards else -1
        if self.color_index > color.MAX_COLOR:
            self.color_index = color.MIN_COLOR
        if self.color_index < color.MIN_COLOR:
            self.color_index = color.MAX_COLOR

    def scale(self, up):
        s = 1.1 if up else 0.9
        self.scaling_matrix = numpy.dot(self.scaling_matrix, scaling([s, s, s]))
        self.aabb.scale(s)


    def translate(self, x, y, z):
        self.translation_matrix = numpy.dot(
            self.translation_matrix,
            translation([x, y, z])
        )

    
    