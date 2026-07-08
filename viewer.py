from primitive import init_primitives
from OpenGL.GL import glCallList, glClear, glClearColor, glColorMaterial, glCullFace, glDepthFunc, glDisable, glEnable,\
                      glFlush, glGetFloatv, glLightfv, glLoadIdentity, glMatrixMode, glMultMatrixf, glPopMatrix, \
                      glPushMatrix, glTranslated, glViewport, \
                      GL_AMBIENT_AND_DIFFUSE, GL_BACK, GL_CULL_FACE, GL_COLOR_BUFFER_BIT, GL_COLOR_MATERIAL, \
                      GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_FRONT_AND_BACK, GL_LESS, GL_LIGHT0, GL_LIGHTING, \
                      GL_MODELVIEW, GL_MODELVIEW_MATRIX, GL_POSITION, GL_PROJECTION, GL_SPOT_DIRECTION
from OpenGL.constants import GLfloat_3, GLfloat_4
from OpenGL.GLU import gluPerspective, gluUnProject
import pygame
from pygame.locals import DOUBLEBUF, OPENGL

import numpy
from numpy.linalg import norm, inv

from interaction import Interaction
from primitive import G_OBJ_PLANE
from sphere import Sphere
from cube import Cube
from snowfigure import SnowFigure
from scene import Scene

class Viewer(object):
    def __init__(self):
        """Initialize the Viewer Class"""
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()

    def init_interface(self):
        """ Initialize the window """
        pygame.init()
        pygame.display.set_mode((640, 480), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Modeller")

    def init_opengl(self):
        """Initialize OpenGL Settings to render the Scene"""
        """First the camera"""
        """Create an array of( n x n )"""
        self.inverseModelView = numpy.identity(4)
        """Enable /Disable various graphics processing on the GPU """
        glEnable(GL_CULL_FACE)
        """Discard polygons based on whether they face toward or away from viewer"""
        glCullFace(GL_BACK)
        """Allow OpenGL to track the depth of each pixel"""
        glEnable(GL_DEPTH_TEST)
        """Specify the depth comparison function, GL_LESS passes if the incoming depth value is less than stored depth value"""
        glDepthFunc(GL_LESS)
        """Enables lighting, identified by the symbolic names of the form GL_LIGHTi where i ranges from 0 to Gl_MAX_LIGHTS - 1"""
        glEnable(GL_LIGHT0)
        """Set position, direction. Prameters(light£, property, array)"""
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0 ,0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))
        """Cause a material color to track the current color"""
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)

    def init_scene(self):
        """Initialize the scene object and initial scene"""
        self.scene = Scene()
        self.create_sample_scene()

    def create_sample_scene(self):
        cube_node  = Cube()
        cube_node.translate(2, 0, 2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)

        sphere_node = Sphere()
        sphere_node.translate(- 2, 0, 2)
        sphere_node.color_index = 3
        self.scene.add_node(sphere_node)

        hierarchical_node = SnowFigure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_node(hierarchical_node)

    def init_interaction(self):
        """Handle/ Initialize user interaction and callbacks"""
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                self.interaction.handle_event(event)
            self.render()
            pygame.display.flip()
            pygame.time.wait(10)

    
    def render(self):
        """"""
        self.init_view()

        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrixf(self.interaction.trackball.matrix)

        """Store the inverse of the current modelview"""
        currentModelView = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX))
        self.modelView = numpy.transpose(currentModelView)
        self.inverseModelView = inv(numpy.transpose(currentModelView))

        """
        Render the scene, This will call the render function for each object in the scene
        """
        self.scene.render()

        #Draw the grid
        glDisable(GL_LIGHTING)
        glCallList(G_OBJ_PLANE)
        glPopMatrix()

            
    def init_view(self):
        surface = pygame.display.get_surface()
        if surface is None:
            return
        xSize, ySize = surface.get_size()
        aspect_ratio = float(xSize) / float(ySize)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)

    def get_ray(self, x, y):
        """
        Generate a ray beginning at the near plane, in the direction that
        the x, y, coordinates are facing

        Consumes:x, y, coordinates of mouse on screen
        Return: start, direction of the ray
        """

        self.init_view()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        start = numpy.array(gluUnProject(x, y, 0.001))
        end = numpy.array(gluUnProject(x, y, 0.999))

        direction = end - start
        direction = direction / norm(direction)

        return (start, direction)
    
    def pick(self, x, y):

        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.modelView)

    def move(self, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.move_selected(start, direction, self.inverseModelView)

    def rotate_color(self, forward):
        self.scene.rotate_selected_color(forward)

    def scale(self, up):
        self.scene.scale_selected(up)

    def place(self, shape, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.place(shape, start, direction, self.inverseModelView)


if __name__ == "__main__":
    viewer = Viewer()
    viewer.main_loop()