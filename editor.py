import circle
import triangle
import rectangle

class Editor:
    def __init__(self):
        self.objects = []
        self.groups = []
        self.selection = None
        
    def reset(self):
        self.objects = []
        self.groups = []
        self.selection = []
        
    def create_circle(self, x, y, rad):
        self.objects.append(circle.Circle(x, y, rad))
            
    def create_triangle(self, x, y, side):
        self.objects.append(triangle.Triangle(x, y, side))
            
    def create_rectangle(self, x, y, side_x, side_y):
        self.objects.append(rectangle.Rectangle(x, y, side_x, side_y))

    def move_object(self, x, y):
        self.objects[self.objects.index(self.selection)].move(x, y)