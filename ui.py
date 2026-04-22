import pygame
from settings import *

class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", 30, bold=True)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=12)
        txt = self.font.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("Georgia", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Georgia", 64, bold=True)

    def draw_hud(self, screen, player):
        pygame.draw.rect(screen, (80, 0, 0), (20, 20, 220, 22), border_radius=8)
        bar_width = int((player.health / PLAYER_MAX_HEALTH) * 220)
        pygame.draw.rect(screen, RED, (20, 20, max(0, bar_width), 22), border_radius=8)
        pygame.draw.rect(screen, WHITE, (20, 20, 220, 22), 2, border_radius=8)

        hp_text = self.small_font.render(f"HP: {player.health}/{PLAYER_MAX_HEALTH}", True, WHITE)
        screen.blit(hp_text, (250, 20))

        controls = self.small_font.render(
            "Move: Left/Right | Jump: Up/Space | Melee: X | Shoot: Z",
            True,
            WHITE
        )
        screen.blit(controls, (20, 52))
