import pygame
import settings

class HUD:

    def __init__(self):
        self.width = 300
        self.height = 100
        self.font = pygame.font.Font(None, 24)
        self.left = settings.SCREEN_WIDTH-self.width

        self.hud_rect = pygame.Rect(self.left, 0, self.width, self.height)

        self.padding = 10
        self.text_color = settings.BLACK
        self.hud_color = (240, 240, 240)
        self.room = settings.StarterRoom
        self.quest = None

    def draw(self, screen):
        self.hud_rect = pygame.Rect(self.left, 0, self.width, self.height)

        pygame.draw.rect(screen, self.hud_color, self.hud_rect)
        pygame.draw.rect(screen, settings.BLACK, self.hud_rect, 2)  # border

        # adds a text that displays the current room
        text = "Current Room: " + self.room.title()
        text_surface = self.font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.hud_rect.x + self.padding, self.hud_rect.y + self.padding))

        if self.quest:
            text = "Current Quest: " + self.quest.title()
            text_surface = self.font.render(text, True, self.text_color)
            screen.blit(text_surface, (self.hud_rect.x + self.padding, self.hud_rect.y + self.padding + 25))

