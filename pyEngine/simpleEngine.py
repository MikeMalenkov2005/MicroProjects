from vector import *
import pygame as pg

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

#GAME CAMERA CLASS
class Camera:
    def __init__(self, position:Vec2, screen):
        self.position = position
        self.screen = screen

#STANDART BODY CLASS
class Body:
    def __init__(self, position:Vec2=Vec2(0, 0), dimension:Vec2=Vec2(0, 0)):
        self.position = position
        self.dimension = dimension

#STATIC CLASS
class Static(Body):
    def __init__(self, position: Vec2, dimension: Vec2, sprite_path:str=None):
        super().__init__(position=position, dimension=dimension)
        if sprite_path:
            self.sprite = pg.image.load(sprite_path).convert_alpha()
        else:
            self.sprite = None
    def draw(self, camera:Camera):
        _draw = self.position.x + self.dimension.x - camera.position.x < Vec2.get(camera.screen.get_size()).x or self.position.x - self.dimension.x - camera.position.x < Vec2.get(camera.screen.get_size()).x or self.position.y + self.dimension.y - camera.position.y < Vec2.get(camera.screen.get_size()).y or self.position.y - self.dimension.y - camera.position.y < Vec2.get(camera.screen.get_size()).y
        if _draw:
            if self.sprite:
                point = self.position - (self.dimension / 2) - camera.position
                camera.screen.blit(self.sprite, pg.Rect(point.x, point.y, self.dimension.x, self.dimension.y))
    def on_collision(self, other:Body):
        pass
    def start(self):
        pass
    def update(self, delta:float):
        pass

#DYNAMIC PHYSICS CLASS
class Dynamic(Body):
    def __init__(self, position: Vec2, dimension: Vec2, sprite_path:str=None):
        super().__init__(position=position, dimension=dimension)
        if sprite_path:
            self.sprite = pg.image.load(sprite_path).convert_alpha()
        else:
            self.sprite = None
    def draw(self, camera:Camera):
        _draw = self.position.x + self.dimension.x - camera.position.x < Vec2.get(camera.screen.get_size()).x or self.position.x - self.dimension.x - camera.position.x < Vec2.get(camera.screen.get_size()).x or self.position.y + self.dimension.y - camera.position.y < Vec2.get(camera.screen.get_size()).y or self.position.y - self.dimension.y - camera.position.y < Vec2.get(camera.screen.get_size()).y
        if _draw:
            if self.sprite:
                point = self.position - (self.dimension / 2) - camera.position
                camera.screen.blit(self.sprite, pg.Rect(point.x, point.y, self.dimension.x, self.dimension.y))
    def on_collision(self, other:Body):
        pass
    def start(self):
        pass
    def update(self, delta:float):
        pass

#PHYSICS SPACE FOR PROCESSING OBJECTS
class Space:
    def __init__(self, map:list[Static]=[], dynamics:list[Dynamic]=[], gravity:Vec2=Vec2(0, 0)):
        self.map:list[Static] = map
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
        for dinamic in self.dynamics:
            for dinamic1 in self.dynamics:
                if dinamic != dinamic1:
                    x = Vec2(1, 0)
                    y = Vec2(0, 1)
                    dinamic.on_collision(dinamic1)
                    dinamic1.on_collision(dinamic)
            for static in self.map:
                dinamic.on_collision(static)
                static.on_collision(dinamic)

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