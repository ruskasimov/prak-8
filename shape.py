class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        
    def dot_inside(self, x, y):
        pass