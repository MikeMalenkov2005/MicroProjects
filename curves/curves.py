import pygame as pg
import numpy as np


# P0 and P1 are points you whant to interpellate between,
# also t must be in the range from 0 to 1
def lerp(P0: tuple, P1: tuple, t: float) -> tuple:
    return tuple(map(lambda a, b: a + b, map(lambda x: (1 - t) * x, P0), map(lambda x: t * x, P1)))


def bezier(points: list, t: float) -> tuple:
    ans = list(points)
    while len(ans) > 1:
        ans = [lerp(ans[i], ans[i + 1], t) for i in range(len(ans) - 1)]
    return ans[0]


def pg_draw_bezier(surface: pg.Surface, color: pg.Color, points: list, width: int = 1, accuracy: int = 0xFFFF) -> pg.Rect:
    actual = [bezier(points, t) for t in np.linspace(0, 1, accuracy)]
    return pg.draw.lines(surface, color, False, list(map(lambda x: (x[0], x[1]), actual)), width)


background_colour = (0, 0, 0)
(width, height) = (640, 480)
screen = pg.display.set_mode((width, height))

pg.display.set_caption('curve test')
screen.fill(background_colour)
pg_draw_bezier(screen, pg.Color(255, 255, 255), [(40, 80), (100, 400), (540, 400), (600, 80)], 4)
pg.display.flip()


running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
