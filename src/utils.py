import pygame as pg


def draw_text(screen, text, color, x, y, center=False, size=20):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def draw_multiline_text(screen, multitext: list, color, x, y, center=False, size=20):
    font = pg.font.SysFont(None, size)
    for text in multitext:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)
        y += text_surface.get_height()
