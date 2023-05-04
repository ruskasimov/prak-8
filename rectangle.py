import shape

class Rectangle(shape.Shape):
    def __init__(self, x, y, side_x, side_y):
        super().__init__(x, y)
        self.side_x = side_x
        self.side_y = side_y
        
    def dot_inside(self, x, y):
        return self.x - self.side_x / 2 < x and x < self.x + self.side_x / 2 and \
            self.y - self.side_y / 2 < y and y < self.y + self.side_y / 2