import shape

class Circle(shape.Shape):
    def __init__(self, x, y, rad):
        super().__init__(x, y)
        self.rad = rad
    
    def dot_inside(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.rad ** 2