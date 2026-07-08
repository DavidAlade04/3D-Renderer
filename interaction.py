from collections import defaultdict
import trackball
import pygame

class Interaction(object):
    def __init__(self):
        """Handle User Interaction"""
        #Currently pressed mouse button
        self.pressed = None
        #The current location of the camera
        self.translation = [0, 0, 0, 0]
        #The trackball to calculate rotation
        self.trackball = trackball.Trackball(theta = -25, distance=15)
        #The current mouse location
        self.mouse_loc = None
        #Unsophisticated callback mechanism
        self.callbacks = defaultdict(list)

    def translate(self, x, y, z):
        """Translate the camera"""
        self.translation[0] += x
        self.translation[1] += y
        self.translation[2] += z

    def handle_event(self, event):
        """Called by the main loop to process a Pygame event"""
        surface = pygame.display.get_surface()
        if surface is None:
            return
        xSize, ySize = surface.get_size()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, screen_y = event.pos
            y = ySize - screen_y # Invert the Y coordinate because OpenGL is inverted
            self.mouse_loc = (x, y)
            self.pressed = event.button
            if event.button == 1: # Left
                self.trigger('pick', x, y)
            elif event.button == 4: # Scroll up
                self.translate(0, 0, 1.0)
            elif event.button == 5: # Scroll down
                self.translate(0, 0, -1.0)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = None
            x, screen_y = event.pos
            y = ySize - screen_y
            self.mouse_loc = (x, y)

        elif event.type == pygame.MOUSEMOTION:
            x, screen_y = event.pos
            y = ySize - screen_y
            if self.pressed is not None and self.mouse_loc is not None:
                dx = x - self.mouse_loc[0]
                dy = y - self.mouse_loc[1]
                if self.pressed == 3 and self.trackball is not None: # Right click
                    self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)
                elif self.pressed == 1: # Left click
                    self.trigger('move', x, y)
                elif self.pressed == 2: # Middle click
                    self.translate(dx/60.0, dy/60.0, 0)
            self.mouse_loc = (x, y)

        elif event.type == pygame.KEYDOWN:
            x, screen_y = pygame.mouse.get_pos()
            y = ySize - screen_y
            
            if event.key == pygame.K_s:
                self.trigger('place', 'sphere', x, y)
            elif event.key == pygame.K_c:
                self.trigger('place', 'cube', x, y)
            elif event.key == pygame.K_f:
                self.trigger('place', 'figure', x, y)
            elif event.key == pygame.K_UP:
                self.trigger('scale', up=True)
            elif event.key == pygame.K_DOWN:
                self.trigger('scale', up=False)
            elif event.key == pygame.K_LEFT:
                self.trigger('rotate_color', forward=True)
            elif event.key == pygame.K_RIGHT:
                self.trigger('rotate_color', forward=False)

    def register_callback(self, name, func):
        self.callbacks[name].append(func)

    def trigger(self, name, *args, **kwargs):
        for func in self.callbacks[name]:
            func(*args, **kwargs)
