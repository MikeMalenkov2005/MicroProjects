import math

def clamp(val:float, _min:float, _max:float):
    return min(_max, max(_min, val))

class Vec2:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return "Vec2" + str((self.x, self.y))
    @staticmethod
    def get(xy:tuple):
        x, y = xy
        return Vec2(x, y)
    def dot(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        return None
    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return None
    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return None
    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)
    def __truediv__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        return Vec2(self.x / other, self.y / other)
    def len(self) -> float:
        return abs(math.sqrt(self.sq_len()))
    def sq_len(self):
        return abs(self.x ** 2 + self.y ** 2)
    def dist(self, other):
        if isinstance(other, Vec2):
            return abs(math.sqrt(self.sq_dist(other)))
        return None
    def sq_dist(self, other):
        if isinstance(other, Vec2):
            return abs((self - other).sq_len())
        return None
    def unit(self):
        l = self.len()
        if l == 0: return Vec2(0, 0)
        return Vec2(self.x, self.y) / l
    def normolize(self):
        unit = self.unit()
        self.x = unit.x
        self.y = unit.y
    def rotated(self, angle:float):
        l = self.len()
        return Vec2(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle)).unit() * l
    def rotate(self, angle:float):
        r = self.rotated(angle)
        self.x = r.x
        self.y = r.y
    def __eq__(self, o) -> bool:
        if isinstance(o, Vec2):
            return (self.x == o.x) and (self.y == o.y)
        return False