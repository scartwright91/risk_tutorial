import pygame as pg

from src.geo import Country, World


class Player:
    def __init__(self, country: Country, world: World, color: tuple) -> None:
        self.country = country
        self.world = world
        self.color = color
        self.country.color = self.color
        self.timer = pg.time.get_ticks()
        self.controlled_countries = [self.country.name]
        self.neighbours = self.get_neighbours()

        # moving units
        self.move_country_from = ""
        self.move_country_to = ""
        self.move_n_units = 0

        # attacking countries
        self.attack_country_from = ""
        self.attack_country_to = ""

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

        now = pg.time.get_ticks()
        
        if self.move_country_from == "":
            for country in self.controlled_countries:
                c = self.world.countries[country]
                if c.hovered and pg.mouse.get_pressed()[0]:
                    self.move_country_from = c.name
                    print(f"Moving from {self.move_country_from}")

        if (self.move_country_to == "") and (self.move_country_from != ""):
            for country in self.controlled_countries:
                c = self.world.countries[country]
                if (c.hovered and pg.mouse.get_pressed()[0] and c.name != self.move_country_from):
                    self.move_country_to = c.name
                    print(f"Moving to {self.move_country_to}")

        if pg.mouse.get_pressed()[2]:
            self.move_country_from = ""
            self.move_country_to = ""
            self.move_n_units = 0

        keys = pg.key.get_pressed()
        if self.move_country_from != "" and self.move_country_to != "":
            c_from = self.world.countries[self.move_country_from]
            c_to = self.world.countries[self.move_country_to]
            if keys[pg.K_UP] and (now - self.timer > 200) and (c_from.units - self.move_n_units > 1):
                self.timer = now
                self.move_n_units += 1
                print(f"Number of units to move: {self.move_n_units}")
            if keys[pg.K_DOWN] and (now - self.tiemr > 200) and (self.move_n_units > 0):
                self.timer = now
                self.move_n_units -= 1
                print(f"Number of units to move: {self.move_n_units}")
            
            if keys[pg.K_RETURN]:
                c_from.units -= self.move_n_units
                c_to.units += self.move_n_units
                print(f"Moved {self.move_n_units} from {self.move_country_from} to {self.move_country_to}")
                self.move_country_from = ""
                self.move_country_to = ""
                self.move_n_units = 0


    def attack_country(self) -> None:
        
        if self.attack_country_from == "":
            for country in self.controlled_countries:
                c = self.world.countries[country]
                if c.hovered and pg.mouse.get_pressed()[0] and (not c.has_attacked):
                    self.attack_country_from = c.name
                    print(f"Attacking from {self.attack_country_from}")

        if (self.attack_country_to == "") and (self.attack_country_from != ""):
            for country in self.world.countries[self.attack_country_from].neighbours:
                if country not in self.controlled_countries:
                    c = self.world.countries[country]
                    if c.hovered and pg.mouse.get_pressed()[0]:
                        self.attack_country_to = c.name
                        print(f"Attacking {self.attack_country_to}")

        # cancel selection
        if pg.mouse.get_pressed()[2]:
            self.attack_country_from = ""
            self.attack_country_to = ""

        # battle
        keys = pg.key.get_pressed()
        if (
            keys[pg.K_RETURN] and (self.attack_country_from != "") and (self.attack_country_to != "")
        ):
            self.world.battle(self.attack_country_from, self.attack_country_to)
            self.attack_country_from = ""
            self.attack_country_to = ""

    def get_neighbours(self) -> list:
        neighbours = []
        for country in self.controlled_countries:
            for neighbour in self.world.countries[country].neighbours:
                if neighbour not in self.controlled_countries:
                    neighbours.append(neighbour)
        return set(neighbours)
    
    def conquer(self, country:str) -> None:
        self.world.countries[country].color = self.color
        self.world.countries[country].controlled_by = self.country.name
        self.controlled_countries.append(country)
        self.neighbours = self.get_neighbours()

    def reset_turn(self) -> None:

        print("Reset turn")
        self.timer = 0

        self.move_country_from = ""
        self.move_country_to = ""
        self.move_n_units = 0

        self.attack_country_from = ""
        self.attack_country_to = ""

        for country in self.controlled_countries:
            c = self.world.countries[country]
            c.has_attacked = False

