import shape

class Triangle(shape.Shape):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.side = side

    def dot_inside(self, x, y):
        x1 = self.x - self.side / 2
        x2 = self.x + self.side / 2
        y1 = self.y + self.side / 2 / 3 ** 0.5
        y2 = self.y - self.side / 3 ** 0.5
        k1 = (y1 - y2) / (x1 - self.x)
        k2 = (y1 - y2) / (x2 - self.x)
        return y < self.y + self.side / 2 / 3 ** 0.5 and \
            y - y2 > k1 * (x - self.x) and y - y2 > k2 * (x - self.x)