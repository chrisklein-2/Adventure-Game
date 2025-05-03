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
        self.cooldown = 1.0
        self.last_attack = 0

        if image: 
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = pygame.Surface((32, 32)) 

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

# creates an enemy based on the name
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

    # moves the enemy around
    def move(self, player):

        # stores current position
        new_rect = self.rect.copy()
        
        dx = player.x - self.x
        dy = player.y - self.y

        # determines movement direction
        if abs(dx) > abs(dy):  
            if dx > 0:
                new_rect.x += self.speed
                self.direction = "right"
            else:
                new_rect.x -= self.speed
                self.direction = "left"
        else:  
            if dy > 0:
                new_rect.y += self.speed
                self.direction = "up"
            else:
                new_rect.y -= self.speed
                self.direction = "down"

        # for player detection
        new_rect.clamp_ip(pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        if player and not new_rect.colliderect(player.rect):
            # makes the move
            self.rect = new_rect

        # when it collides with a player
        else:
            current_time = time.time() # for the attack cooldown
            if current_time - self.last_attack >= self.cooldown:
                player.health -= self.attack
                self.last_attack = current_time
        # updates enemy location
        self.x, self.y = self.rect.x, self.rect.y


# subclass for a goblin
class Goblin(Enemy):
    def __init__(self, name="goblin", health=20, attack=5):
        super().__init__(name, health, attack)

# subclass for ork
class Ork(Enemy):
    def __init__(self, name="ork", health=40, attack=10):
        super().__init__(name, health, attack)
