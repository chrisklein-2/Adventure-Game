import pygame
import json
import time
import random
import settings

class NPC(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dialogue=None, image=None):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.dialogue = dialogue
        self.dialogue_index = 0
        self.direction = None
        self.speed = 1
        self.last_move = time.time()
        self.move_interval = random.uniform(1,3)
        
        if image: 
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = pygame.Surface((32, 32))  # default placeholder size for NPC
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        

    def check_next_line(self):
        if self.dialogue_index < len(self.dialogue):
            return True
        else:
            return False  # dialogue finished

    def reset_dialogue(self):
        self.dialogue_index = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def interact(self, text_box):
        text_box.show(f"{self.name}: {self.dialogue[self.dialogue_index]}")
        self.dialogue_index += 1

    def wander(self, player):

        # chooses which direction to go at random given an intervel of time
        current_time = time.time()
        if current_time - self.last_move > self.move_interval:
            self.direction = random.choice(["up", "down", "left", "right", None])
            self.move_interval = random.uniform(1, 3)
            self.last_move = current_time
        
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


# loads in npcs as a dictionary
def load_npcs():
    with open("data/npcs.json", "r") as f:
        data = json.load(f)
    
    npc_dict = {}
    for npc_name, npc_data in data.items():
        npc = NPC(
            name=npc_data["name"],
            x=npc_data["x"],
            y=npc_data["y"],
            dialogue=npc_data["dialogue"],
            image=npc_data.get("image")
        )
        npc_dict[npc_name] = npc
    return npc_dict