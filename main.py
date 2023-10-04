import pygame as pg
import sys

from src.game import Game


pg.init()
pg.mixer.init()
pg.font.init()

WIDTH = 1280
HEIGHT = 720
window_size = pg.Vector2(WIDTH, HEIGHT)

screen = pg.display.set_mode(window_size)
clock = pg.time.Clock()

pg.display.set_caption("Risk")

game = Game(screen, clock, window_size)
game.run()

pg.quit()
sys.exit()
