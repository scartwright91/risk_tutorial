import pygame as pg

from src.geo import World
from src.player import Player


class Game:
    def __init__(
        self, screen: pg.Surface, clock: pg.time.Clock, window_size: pg.Vector2
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.playing = True
        self.phase = "place_units"
        self.world = World()
        self.player = Player(
            self.world.countries.get("France"), self.world, (0, 0, 255)
        )

    def run(self) -> None:
        while self.playing:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.events()
            self.update()
            self.draw()
            pg.display.update()

    def events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False

    def update(self) -> None:
        self.world.update()
        self.player.update(self.phase)

    def draw(self) -> None:
        self.world.draw(self.screen)
