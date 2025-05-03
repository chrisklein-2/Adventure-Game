import pygame
import time
import random
import settings

class Enemy:
    def __init__(self, name, health, attack, image = None):
        self.name = name
        self.health = health
        self.alive = True
        self.attack = attack
        self.x = random.randint(0, settings.SCREEN_WIDTH-64) # -64 to adjust for size of enemy
        self.y = random.randint(0, settings.SCREEN_HEIGHT-64)
        self.direction = None
        self.speed = 1
        self.last_move = time.time()
        self.move_interval = random.uniform(1,3)

        if image: 
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = pygame.Surface((32, 32))  # default placeholder size for NPC

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# subclass for a goblin
class Goblin(Enemy):
    def __init__(self, name="Goblin", health=20, attack=5):
        super().__init__(name, health, attack)
