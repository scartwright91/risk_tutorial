import pygame as pg

from src.geo import World
from src.player import Player
from src.utils import draw_text


class Game:
    def __init__(
        self, screen: pg.Surface, clock: pg.time.Clock, window_size: pg.Vector2
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.font = pg.font.SysFont(None, 24)
        self.playing = True
        self.phases = ["place_units", "move_units", "attack_country"]
        self.phase_idx = 0
        self.phase = self.phases[self.phase_idx]
        self.phase_timer = pg.time.get_ticks()
        self.world = World()
        self.player = Player(
            self.world.countries.get("France"), self.world, (0, 0, 255)
        )
        self.create_phase_ui()

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
        now = pg.time.get_ticks()
        self.world.update()
        self.player.update(self.phase)
        if self.world.battle_res is not None:
            # resolve battle
            if self.world.battle_res["victory"]:
                if self.world.battle_res["attacking_country"] in self.player.controlled_countries:
                    self.player.conquer(self.world.battle_res["defending_country"])
            print(self.world.battle_res)
            self.world.battle_res = None

        self.finish_phase_button_hovered = False
        if self.finish_phase_button.collidepoint(pg.mouse.get_pos()):
            self.finish_phase_button_hovered = True

        if self.finish_phase_button_hovered:
            if pg.mouse.get_pressed()[0] and (now - self.phase_timer > 500):
                self.phase_timer = now
                self.phase_idx = (self.phase_idx + 1) % len(self.phases)
                self.phase = self.phases[self.phase_idx]
                if self.phase == "place_units":
                    self.player.reset_turn()

    def draw(self) -> None:
        self.world.draw(self.screen)
        self.draw_phase_ui()
        text_surface = self.font.render(
            f"FPS: {int(self.clock.get_fps())}", False, (255, 255, 255)
        )
        self.screen.blit(text_surface, (10, 10))

    def create_phase_ui(self) -> None:
        self.current_phase_image = pg.Surface((200, 50))
        self.current_phase_image.fill((25, 42, 86))
        self.current_phase_rect = self.current_phase_image.get_rect(topleft=(10, 10))

        self.finish_phase_image = pg.Surface((200, 50))
        self.finish_phase_image.fill((25, 42, 86))
        self.finish_phase_button = self.finish_phase_image.get_rect(topleft=(10, 70))
        self.finish_phase_button_hovered = False

    def draw_phase_ui(self) -> None:
        self.screen.blit(self.current_phase_image, self.current_phase_rect)
        if self.phase == "place_units":
            draw_text(
                self.screen,
                self.font,
                "Place",
                (255, 255, 255),
                self.current_phase_rect.centerx,
                self.current_phase_rect.centery,
                True,
            )
        elif self.phase == "move_units":
            draw_text(
                self.screen,
                self.font,
                "Move",
                (255, 255, 255),
                self.current_phase_rect.centerx,
                self.current_phase_rect.centery,
                True,
            )
        elif self.phase == "attack_country":
            draw_text(
                self.screen,
                self.font,
                "Attack",
                (255, 255, 255),
                self.current_phase_rect.centerx,
                self.current_phase_rect.centery,
                True,
            )

        if self.finish_phase_button_hovered:
            self.finish_phase_image.fill((255, 0, 0))
        else:
            self.finish_phase_image.fill((25, 42, 86))

        self.screen.blit(self.finish_phase_image, self.finish_phase_button)
        draw_text(
            self.screen,
            self.font,
            "Finish phase",
            (255, 255, 255),
            self.finish_phase_button.centerx,
            self.finish_phase_button.centery,
            True,
        )
