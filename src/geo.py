import json
import pygame as pg
import random
from pandas import Series

from shapely.geometry import Point, Polygon

from src.utils import draw_text, draw_multiline_text


class Country:
    def __init__(self, name: str, coords: list) -> None:
        self.name = name
        self.coords = coords
        self.font = pg.font.SysFont(None, 24)
        self.polygon = Polygon(self.coords)
        self.center = self.get_center()
        self.units = random.randint(1, 3)
        self.color = (72, 126, 176)
        self.hovered = False
        self.neighbours = None

    def update(self, mouse_pos: pg.Vector2) -> None:
        self.hovered = False
        if Point(mouse_pos.x, mouse_pos.y).within(self.polygon):
            self.hovered = True

    def draw(self, screen: pg.Surface, scroll: pg.Vector2) -> None:
        pg.draw.polygon(
            screen,
            (255, 0, 0) if self.hovered else self.color,
            [(x - scroll.x, y - scroll.y) for x, y in self.coords],
        )
        pg.draw.polygon(
            screen,
            (255, 255, 255),
            [(x - scroll.x, y - scroll.y) for x, y in self.coords],
            width=1,
        )
        draw_text(
            screen,
            self.font,
            str(self.units),
            (255, 255, 255),
            self.center.x - scroll.x,
            self.center.y - scroll.y,
            True,
        )

    def get_center(self) -> pg.Vector2:
        return pg.Vector2(
            Series([x for x, y in self.coords]).mean(),
            Series([y for x, y in self.coords]).mean(),
        )


class World:
    MAP_WIDTH = 2.05 * 4000
    MAP_HEIGHT = 1.0 * 4000

    def __init__(self) -> None:
        self.read_geo_data()
        self.countries = self.create_countries()
        self.create_neighbours()
        self.scroll = pg.Vector2(3650, 395)
        self.font = pg.font.SysFont(None, 24)

        # hovering countries panel
        self.hovered_country = None
        self.hover_surface = pg.Surface((300, 100), pg.SRCALPHA)
        self.hover_surface.fill((25, 42, 86, 155))

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
            country.draw(screen, self.scroll)
        if self.hovered_country is not None:
            self.draw_hovered_country(screen)

    def update(self) -> None:
        self.update_camera()
        mouse_pos = pg.mouse.get_pos()
        self.hovered_country = None
        for country in self.countries.values():
            country.update(
                pg.Vector2(mouse_pos[0] + self.scroll.x, mouse_pos[1] + self.scroll.y)
            )
            if country.hovered:
                self.hovered_country = country

    def update_camera(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.scroll.x -= 10
        elif keys[pg.K_d]:
            self.scroll.x += 10

        if keys[pg.K_w]:
            self.scroll.y -= 10
        elif keys[pg.K_s]:
            self.scroll.y += 10

        if keys[pg.K_SPACE]:
            self.scroll = pg.Vector2(3650, 395)

    def draw_hovered_country(self, screen: pg.Surface) -> None:
        screen.blit(self.hover_surface, (1280 - 310, 720 - 110))
        draw_text(
            screen,
            self.font,
            self.hovered_country.name,
            (255, 255, 255),
            1280 - 310 / 2,
            720 - 100,
            True,
            24,
        )
        draw_multiline_text(
            screen,
            self.font,
            [f"Units: {str(self.hovered_country.units)}"],
            (255, 255, 255),
            1280 - 310 + 5,
            720 - 90 + 5,
            False,
            20,
        )

    def create_neighbours(self) -> None:
        for k, v in self.countries.items():
            v.neighbours = self.get_country_neighbours(k)

    def get_country_neighbours(self, country: str) -> list:
        neighbours = []
        country_poly = self.countries[country].polygon
        for other_country_key, other_country_value in self.countries.items():
            if country != other_country_key:
                if country_poly.intersects(other_country_value.polygon):
                    neighbours.append(other_country_key)
        if country == "United Kingdom":
            neighbours += ["Ireland", "France", "Iceland"]
        elif country == "Ireland":
            neighbours += ["United Kingdom", "Iceland"]
        elif country == "Iceland":
            neighbours += ["United Kingdom", "Ireland"]
        elif country == "France":
            neighbours += ["United Kingdom"]
        elif country == "Denmark":
            neighbours += ["Norway", "Sweden"]
        elif country == "Norway":
            neighbours += ["Denmark"]
        elif country == "Sweden":
            neighbours += ["Denmark"]
        elif country == "Finland":
            neighbours += ["Estonia"]
        elif country == "Estonia":
            neighbours += ["Finland"]
        return neighbours
