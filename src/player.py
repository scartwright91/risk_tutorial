import pygame as pg

from src.geo import Country, World


class Player:
    def __init__(self, country: Country, world: World, color: tuple) -> None:
        self.country = country
        self.world = world
        self.color = color
        self.country.color = self.color
        self.timer = pg.time.get_ticks()
        self.controlled_countries = [self.country.name, "Spain"]
        self.neighbours = self.get_neighbours()
        print(self.neighbours)

    def update(self, phase: str) -> None:
        if phase == "place_units":
            self.place_units()
        elif phase == "move_units":
            self.move_units()
        elif phase == "attack_country":
            self.attack_country()

    def place_units(self) -> None:
        now = pg.time.get_ticks()
        for country in self.controlled_countries:
            c = self.world.countries[country]
            if c.hovered and pg.mouse.get_pressed()[0] and (now - self.timer > 300):
                self.timer = now
                c.units += 1

    def move_units(self) -> None:
        pass

    def attack_country(self) -> None:
        pass

    def get_neighbours(self) -> list:
        neighbours = []
        for country in self.controlled_countries:
            for neighbour in self.world.countries[country].neighbours:
                if neighbour not in self.controlled_countries:
                    neighbours.append(neighbour)
        return set(neighbours)
