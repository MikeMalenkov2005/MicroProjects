from vector import *
from collision import *
import pygame as pg

#CONSTANTS
CCC = 0
CPC = 1
PCC = 2
PPC = 3

#RANDOM
class Random:
    seed = 0
    subseed = 0
    @staticmethod
    def get_seed():
        return Random.seed
    @staticmethod
    def set_seed(seed):
        Random.seed = clamp(seed, -500000000, 500000000)
        Random.subseed = clamp((Random.seed + 500000000) / 1000000000, 0, 1)
    @staticmethod
    def rnd():
        x = (Random.subseed + math.pi) ** 8
        Random.subseed = x - int(x)
        return Random.subseed

#INPUT
class Input:
    KEYS:dict = {}
    JUST_KEYS:dict = {}
    @staticmethod
    def update_keys():
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN:
                Input.KEYS[pg.key.name(event.key)] = True
                Input.JUST_KEYS[pg.key.name(event.key)] = True
            if event.type == pg.KEYUP:
                Input.KEYS[pg.key.name(event.key)] = False
                Input.JUST_KEYS[pg.key.name(event.key)] = False
    @staticmethod
    def key_pressed(key:str):
        if key in Input.KEYS:
            return Input.KEYS[key]
        return False
    @staticmethod
    def get_mouse_position():
        return Vec2.get(pg.mouse.get_pos())
    @staticmethod
    def key_just_pressed(key:str):
        if key in Input.JUST_KEYS:
            out = Input.JUST_KEYS[key]
            Input.JUST_KEYS[key] = False
            return out
        return False

#GAME CAMERA
class Camera:
    def __init__(self, position:Vec2, screen) -> None:
        self.position = position
        self.screen = screen

#STATIC OBJECT
class Brash(Body):
    def __init__(self, position:Vec2 = Vec2(0, 0), rotation:float=0, elasticity:float=0, shape:Shape=Shape(), color:pg.Color=pg.Color(0, 0, 0)):
        super().__init__(position=position, rotation=rotation, shape=shape, elasticity=elasticity)
        self.color = color
    def draw(self, camera:Camera):
        if len(self.shape.polygon) == 0:
            pg.draw.circle(camera.screen, self.color, (self.position.x-camera.position.x+Vec2.get(camera.screen.get_size()).x/2, self.position.y-camera.position.y+Vec2.get(camera.screen.get_size()).y/2), self.shape.r)
        else:
            pg.draw.polygon(camera.screen, self.color, [(point.x+self.position.x-camera.position.x+Vec2.get(camera.screen.get_size()).x/2, point.y+self.position.y-camera.position.y+Vec2.get(camera.screen.get_size()).y/2) for point in self.shape.polygon])
    def on_collision(self, other:Body):
        pass
    def start(self):
        pass
    def update(self, delta:float):
        pass

#DYNAMIC PHYSICS OBJECT
class Dynamic(Body):
    def __init__(self, position:Vec2=Vec2(0, 0), rotation:float=0, mass:float=0, elasticity:float=0, shape:Shape=Shape(), color:pg.Color=pg.Color(0, 0, 0)):
        super().__init__(position=position, rotation=rotation, shape=shape, elasticity=elasticity)
        self.mass = mass
        self.velocity:Vec2 = Vec2(0, 0)
        self.angular_velocity:float = 0
        self.actual_rotation:float = 0
        self.color = color
    def draw(self, camera:Camera):
        if len(self.shape.polygon) == 0:
            pg.draw.circle(camera.screen, self.color, (self.position.x-camera.position.x+Vec2.get(camera.screen.get_size()).x/2, self.position.y-camera.position.y+Vec2.get(camera.screen.get_size()).y/2), self.shape.r)
        else:
            pg.draw.polygon(camera.screen, self.color, [(point.x+self.position.x-camera.position.x+Vec2.get(camera.screen.get_size()).x/2, point.y+self.position.y-camera.position.y+Vec2.get(camera.screen.get_size()).y/2) for point in self.shape.polygon])
    def on_collision(self, other:Body):
        pass
    def start(self):
        pass
    def update(self, delta:float):
        self.position += self.velocity * delta
        self.rotation += self.angular_velocity * delta
        for point in self.shape.polygon:
            point.rotate(self.rotation - self.actual_rotation)
        self.actual_rotation = self.rotation
    def rotate(self, angle:float):
        self.rotation += angle
        for point in self.shape.polygon:
            point.rotate(self.rotation - self.actual_rotation)
        self.actual_rotation = self.rotation

#PHYSICS SPACE FOR PROCESSING OBJECTS
class Space:
    def __init__(self, map:list[Brash]=[], dynamics:list[Dynamic]=[], gravity:Vec2=Vec2(0, 0)):
        self.map:list[Brash] = map
        self.dynamics:list[Dynamic] = dynamics
        self.gravity = gravity
    def draw(self, camera:Camera):
        for brash in self.map:
            brash.draw(camera)
        for prop in self.dynamics:
            prop.draw(camera)
    def step(self, delta:float):
        for i in range(len(self.dynamics)):
            if self.dynamics[i] == None: continue
            if self.dynamics[i].remove: self.dynamics[i] = None
        for i in range(len(self.map)):
            if self.map[i] == None: continue
            if self.map[i].remove: self.map[i] = None
        if None in self.dynamics:
            self.dynamics.remove(None)
        if None in self.map:
            self.map.remove(None)
        for prop in self.dynamics:
            if prop == None: continue
            prop.velocity += self.gravity * delta
            prop.update(delta)
        for prop in self.dynamics:
            if prop == None: continue
            for prop1 in self.dynamics:
                if prop1 == None: continue
                if prop == prop1: continue
                collision = get_collision(prop, prop1)
                if collision.colliding:
                    prop.on_collision(prop1)
                    prop1.on_collision(prop)
                    if collision.distance == 0:continue
                    el = (prop.elasticity + prop.elasticity) / 2
                    t = collision.type
                    m0 = prop.mass
                    m1 = prop1.mass
                    if t == CCC:
                        prop.position += collision.vecs0 / (m0 + m1) * m1
                        prop1.position += collision.vecs1 / (m0 + m1) * m0
                        v = collision.vecs0.unit()
                        vr = v.rotated(-math.pi / 2)
                        v0i = v.dot(prop.velocity)
                        v1i = v.dot(prop1.velocity)
                        v0f = (((m0 - m1) / (m0 + m1) * v0i) + (2 * m1 / (m0 + m1) * v1i)) * el
                        v1f = ((2 * m0 / (m0 + m1) * v0i) + ((m1 - m0) / (m0 + m1) * v1i)) * el
                        prop.velocity = v * v0f + vr * vr.dot(prop.velocity)
                        prop1.velocity = v * v1f + vr * vr.dot(prop1.velocity)
                    elif t == CPC:
                        prop.position += collision.vecs0
                        pass
                    elif t == PCC:
                        prop1.position += collision.vecs1
                        pass
                    elif t == PPC:
                        pass
            for brash in self.map:
                collision = get_collision(prop, brash)
                if collision.colliding:
                    prop.on_collision(brash)
                    brash.on_collision(prop)
                    if collision.distance == 0:continue
                    el = prop.elasticity + brash.elasticity
                    t = collision.type
                    m0 = prop.mass
                    if t == CCC or t == CPC:
                        prop.position += collision.vecs0
                        v = collision.vecs0.unit()
                        vr:Vec2 = v.rotated(-math.pi / 2)
                        v0i = v.dot(prop.velocity)
                        v0f = m0 / m0 * v0i * el
                        prop.velocity = v * v0f + vr * vr.dot(prop.velocity)
                    elif t == PCC or t == PPC:
                        vc = collision.vecs0.unit()
                        v = (collision.points0 * -1).unit()
                        vr:Vec2 = v.rotated(-math.pi / 2)
                        ar = vr.dot(collision.vecs0)
                        prop.position += v * v.dot(collision.vecs0)
                        prop.rotate(ar)
                        v0i = vc.dot(vr * collision.points0.len() * prop.angular_velocity + prop.velocity)
                        _v0f = m0 / m0 * v0i * el
                        r0f = vr.dot(vc * _v0f) + ar
                        a = 0
                        b = 0
                        if prop.angular_velocity != 0:a = prop.angular_velocity / abs(prop.angular_velocity)
                        if ar != 0:b = ar / abs(ar)
                        if a == b:
                            r0f += prop.angular_velocity
                        v0f = v.dot(vc * _v0f)
                        prop.angular_velocity = r0f
                        prop.velocity = v * v0f + vr * vr.dot(prop.velocity)

#APP CLASS
class App:
    def __init__(self, space:Space, camera:Camera, name:str, bg:pg.Color):
        pg.init()
        self.name = name
        self.camera = camera
        self.clock = pg.time.Clock()
        self.space = space
        self.bg = bg
    def change_space(self, scene):
        self.scene = scene
    def start(self):
        self.screen_size = Vec2.get(self.camera.screen.get_size())
    def update(self, delta:float):
        self.camera.screen.fill(self.bg)
        self.space.step(delta)
        self.space.draw(self.camera)
    def run(self):
        Input.update_keys()
        self.start()
        Input.update_keys()
        while True:
            Input.update_keys()
            self.update(0.02)
            Input.update_keys()
            if Input.key_pressed("escape"):
                exit()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.name))
            pg.display.flip()
            self.clock.tick()