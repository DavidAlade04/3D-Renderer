from primitive import Primitive, G_OBJ_SPHERE

class Sphere(Primitive):
    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_SPHERE

        