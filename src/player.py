import pygame as pg

from src.geo import Country, World


class Player:
    def __init__(self, country: Country, world: World, color: tuple) -> None:
        self.country = country
        self.world = world
        self.color = color
        self.country.color = self.color
        self.timer = pg.time.get_ticks()

    def update(self, phase: str) -> None:
        if phase == "place_units":
            self.place_units()
        elif phase == "move_units":
            self.move_units()
        elif phase == "attack_country":
            self.attack_country()

    def place_units(self) -> None:
        now = pg.time.get_ticks()
        if pg.mouse.get_pressed()[0] and (now - self.timer > 300):
            self.timer = now
            self.country.units += 1

    def move_units(self) -> None:
        pass

    def attack_country(self) -> None:
        pass
