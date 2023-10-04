import json
import pygame as pg


class Country:
    def __init__(self, name: str, coords: list) -> None:
        self.name = name
        self.coords = coords

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(
            screen, (72, 126, 176), [(x - 3650, y - 395) for x, y in self.coords]
        )
        pg.draw.polygon(
            screen,
            (255, 255, 255),
            [(x - 3650, y - 395) for x, y in self.coords],
            width=1,
        )


class World:
    MAP_WIDTH = 2.05 * 4000
    MAP_HEIGHT = 1.0 * 4000

    def __init__(self) -> None:
        self.read_geo_data()
        self.countries = self.create_countries()

    def read_geo_data(self) -> None:
        with open("./data/country_coords.json", "r") as f:
            self.geo_data = json.load(f)

    def create_countries(self) -> dict:
        countries = {}
        for name, coords in self.geo_data.items():
            xy_coords = []
            for coord in coords:
                x = (self.MAP_WIDTH / 360) * (180 + coord[0])
                y = (self.MAP_HEIGHT / 180) * (90 - coord[1])
                xy_coords.append(pg.Vector2(x, y))
            countries[name] = Country(name, xy_coords)
        return countries

    def draw(self, screen: pg.Surface) -> None:
        for country in self.countries.values():
            country.draw(screen)
