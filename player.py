import pygame
import settings

# Player class
class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(x, y, 20, 20)  # Rect for collision detection
        self.color = (0, 0, 255)  # Blue color for the player


    def update(self, keys, npc=None):
        self.handle_movement(keys)
        if npc:
            self.handle_interaction(keys, npc)

    #lets the player move around with arrow keys
    def handle_movement(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += settings.PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= settings.PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += settings.PLAYER_SPEED
        
        # Update player's rect position after moving
        self.rect.x = self.x
        self.rect.y = self.y

    #draws the player
    def draw(self, screen):
        pygame.draw.rect(screen, settings.BLUE, self.rect)

    def handle_interaction(self, keys, npc):
        if keys[pygame.K_e] and self.rect.colliderect(npc):
            print("Interacted")

    # player.py
    def reset_position(self, direction=None):
        if direction == "south":
            self.y = settings.SCREEN_HEIGHT - 20
        elif direction == "north":
            self.y = 0
        elif direction == "east":
            self.x = 0
        elif direction == "west":
            self.x = settings.SCREEN_WIDTH - 20
        else:
            self.rect.x, self.rect.y = settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2
