import pygame
import time
import random
import settings
import json

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

    def create_enemy(name):
        
        enemy_classes = {
            "goblin": Goblin,
            "ork": Ork,
        }

        enemy_class = enemy_classes.get(name.lower())
        if enemy_class:
            return enemy_class()
        else:
            raise ValueError(f"No enemy type found for name '{name}'")

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self, player):
        # stores current position
        new_rect = self.rect.copy()
        
        # makes the possible npc move
        if self.direction == "up":
            new_rect.y -= self.speed
        elif self.direction == "down":
            new_rect.y += self.speed
        elif self.direction == "left":
            new_rect.x -= self.speed
        elif self.direction == "right":
            new_rect.x += self.speed

        # makes sure it doesn't colide with player
        new_rect.clamp_ip(pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        if player and not new_rect.colliderect(player.rect):
            # makes the move
            self.rect = new_rect

# subclass for a goblin
class Goblin(Enemy):
    def __init__(self, name="goblin", health=20, attack=5):
        super().__init__(name, health, attack)

class Ork(Enemy):
    def __init__(self, name="ork", health=40, attack=10):
        super().__init__(name, health, attack)
