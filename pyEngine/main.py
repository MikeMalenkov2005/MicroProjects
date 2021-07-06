from engine import *

#GAME CONSTANTS
speed = 64
jump = 128

#SPACE CREATION BGN
space = Space()
#DYNAMICS BGN
player = Dynamic(mass=1, elasticity=1, shape=Shape(0, [Vec2(10, 10), Vec2(-10, 10), Vec2(-10, -10), Vec2(10, -10)]), color=pg.Color(255, 127, 0))
#DYNAMICS END
#MAP BGN
grass = Brash(position=Vec2(0, 100), elasticity=0, shape=Shape(50), color=pg.Color(0, 255, 127))
#MAP END
space.dynamics = [player]
space.map = [grass]
space.gravity = Vec2(0, 100)
#SPACE CREATION END
class Game(App):
    def start(self):
        return super().start()
    def update(self, delta):
        motion = Vec2(0, player.velocity.y)
        if Input.key_pressed("d"):motion.x+=speed
        if Input.key_pressed("a"):motion.x-=speed
        if Input.key_just_pressed("space"):motion.y=-jump
        player.velocity = motion
        return super().update(delta)

if __name__ == '__main__':
    app = Game(space, Camera(Vec2(0, 0), pg.display.set_mode((0, 0), pg.FULLSCREEN)), "MyGame", pg.Color(0, 0, 0))
    app.run()