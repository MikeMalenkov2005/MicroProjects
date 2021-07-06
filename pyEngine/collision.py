from vector import *

def line_segment_to_point_vec(p:Vec2, a:Vec2, b:Vec2) -> Vec2:
    pa:Vec2 = p - a
    ba:Vec2 = b - a
    h:float = clamp(pa.dot(ba) / ba.dot(ba), 0, 1)
    return pa - (ba * h)

def point_in_polygon(p:Vec2, poly:list[Vec2]) -> bool:
    if len(poly) > 2:
        n = len(poly)
        count = 0
        x = p.x
        y = p.y
        for i in range(n):
            j = i+1
            if j == n: j = 0
            x1 = poly[i].x
            x2 = poly[j].x
            y1 = poly[i].y
            y2 = poly[j].y
            if ((y < y1) != (y < y2)) and (x < ((x2-x1) * (y-y1) / (y2-y1) + x1)): count += 1
        return (count % 2) == 1
    return False

class Shape:
    def __init__(self, r:float=0, polygon:list[Vec2]=[]):
        self.r = abs(r)
        self.polygon = polygon
        if len(self.polygon) > 2:
            c = Vec2(0, 0)
            for vertex in self.polygon:
                c += vertex
            c = c/len(self.polygon)
            for i in range(len(self.polygon)):
                self.polygon[i] = self.polygon[i] - c
                l = self.polygon[i].len()
                if l > self.r:
                    self.r = l

class Body:
    def __init__(self, position:Vec2=Vec2(0, 0), rotation:float=0, shape:Shape=Shape(), elasticity:float=0):
        self.position = position
        self.rotation = rotation
        self.shape = shape
        self.remove = False
        self.elasticity = clamp(elasticity, 0, 1)

class Collision:
    def __init__(self, colliding:bool, distance:float=None, points0:Vec2=Vec2(0, 0), points1:Vec2=Vec2(0, 0), vecs0:Vec2=Vec2(0, 0), vecs1:Vec2=Vec2(0, 0), type:int=0):
        self.colliding = colliding
        self.distance = distance
        self.points0 = points0
        self.points1 = points1
        self.vecs0 = vecs0
        self.vecs1 = vecs1
        self.type = type
    def __str__(self) -> str:
        return "Collision(" + str(self.colliding) + " " + str(self.distance) + " " + str(self.points0) + " " + str(self.points1) + " " + str(self.vecs0) + " " + str(self.vecs1) + ")"

def CircleCircle(c0:Body, c1:Body) -> Collision:
    l = c0.shape.r + c1.shape.r - c0.position.dist(c1.position)
    v = (c1.position - c0.position).unit()
    return Collision(l>0, l, v * c0.shape.r, v * -c1.shape.r, v * -l, v * l, 0)

def CirclePolygon(c:Body, p:Body) -> Collision:
    is_col = False
    l = -1
    p0 = Vec2(0, 0)
    p1 = Vec2(0, 0)
    v0 = Vec2(0, 0)
    v1 = Vec2(0, 0)
    for i in range(len(p.shape.polygon)):
        j = i+1
        if j == len(p.shape.polygon): j = 0
        v = line_segment_to_point_vec(c.position-p.position, p.shape.polygon[i], p.shape.polygon[j])
        u = v.unit()
        _l = c.shape.r - v.len()
        if (l < 0 or l < _l) and _l >= 0:
            is_col = True
            l = _l
            p0 = u * -c.shape.r
            p1 = (p0 + (u * l)) + c.position - p.position
            v0 = u * l
            v1 = u * -l
    return Collision(is_col, l, p0, p1, v0, v1, 1)

def PolygonCircle(p:Body, c:Body) -> Collision:
    is_col = False
    l = -1
    p0 = Vec2(0, 0)
    p1 = Vec2(0, 0)
    v0 = Vec2(0, 0)
    v1 = Vec2(0, 0)
    for i in range(len(p.shape.polygon)):
        j = i+1
        if j == len(p.shape.polygon): j = 0
        v = line_segment_to_point_vec(c.position-p.position, p.shape.polygon[i], p.shape.polygon[j])
        u = v.unit()
        _l = c.shape.r - v.len()
        if (l < 0 or l < _l) and _l >= 0:
            is_col = True
            l = _l
            p0 = u * -c.shape.r
            p1 = (p0 + (u * l)) + c.position - p.position
            v0 = u * l
            v1 = u * -l
    return Collision(is_col, l, p1, p0, v1, v0, 2)

def PolygonPolygon(p0:Body, p1:Body) -> Collision:
    is_col = False
    l = -2
    _p0:list[Vec2] = []
    _p1:list[Vec2] = []
    v0:list[Vec2] = []
    v1:list[Vec2] = []
    for point in p0.shape.polygon:
        if point_in_polygon(point + p0.position - p1.position, p1.shape.polygon):
            is_col = True
            _l = -1
            p0_ = Vec2(0, 0)
            p1_ = Vec2(0, 0)
            v0_ = Vec2(0, 0)
            v1_ = Vec2(0, 0)
            for i in range(len(p1.shape.polygon)):
                j = i + 1
                if j == len(p1.shape.polygon): j = 0
                lv = line_segment_to_point_vec(point + p0.position - p1.position, p1.shape.polygon[i], p1.shape.polygon[j])
                l_ = lv.len()
                if _l < 0 or _l < l_:
                    _l = l_
                    p0_ = point
                    p1_ = point - lv + p0.position - p1.position
                    v0_ = lv
                    v1_ = lv * -1
            if l < 0 or l <= _l:
                if l < _l:
                    l = _l
                    _p0 = []
                    _p1 = []
                    v0 = []
                    v1 = []
                _p0.append(p0_)
                _p1.append(p1_)
                v0.append(v0_)
                v1.append(v1_)
    for point in p1.shape.polygon:
        if point_in_polygon(point + p1.position - p0.position, p0.shape.polygon):
            is_col = True
            _l = -1
            p0_ = Vec2(0, 0)
            p1_ = Vec2(0, 0)
            v0_ = Vec2(0, 0)
            v1_ = Vec2(0, 0)
            for i in range(len(p0.shape.polygon)):
                j = i + 1
                if j == len(p0.shape.polygon): j = 0
                lv = line_segment_to_point_vec(point + p1.position - p0.position, p0.shape.polygon[i], p0.shape.polygon[j])
                l_ = lv.len()
                if _l < 0 or _l < l_:
                    _l = l_
                    p1_ = point
                    p0_ = point - lv + p0.position - p1.position
                    v1_ = lv
                    v0_ = lv * -1
            if l < 0 or l <= _l:
                if l < _l:
                    l = _l
                    _p0 = []
                    _p1 = []
                    v0 = []
                    v1 = []
                _p0.append(p0_)
                _p1.append(p1_)
                v0.append(v0_)
                v1.append(v1_)
    n = len(_p0)
    if n > 1:
        p0f = line_segment_to_point_vec(Vec2(0, 0), _p0[0], _p0[1]) * -1
        _p0 = [p0f]
        v0f = Vec2(0, 0)
        for vec in v0:
            v0f += vec
        v0 = [v0f / n]
        p1f = line_segment_to_point_vec(Vec2(0, 0), _p1[0], _p1[1]) * -1
        _p1 = [p1f]
        v1f = Vec2(0, 0)
        for vec in v1:
            v1f += vec
        v1 = [v1f / n]
    if n > 0:return Collision(is_col, l, _p0[0], _p1[0], v0[0], v1[0], 3)
    return Collision(is_col)

def get_collision(a:Body, b:Body) -> Collision:
    r = a.shape.r + b.shape.r
    r *= r
    if r < a.position.sq_dist(b.position):
        return Collision(False)
    if len(a.shape.polygon) > 2 and len(b.shape.polygon) > 2:
        return PolygonPolygon(a, b)
    elif len(b.shape.polygon) > 2:
        return CirclePolygon(a, b)
    elif len(a.shape.polygon) > 2:
        return PolygonCircle(a, b)
    return CircleCircle(a, b)