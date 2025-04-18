import pygame
import json

class NPC(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dialogue=None, image=None):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.dialogue = dialogue if dialogue else "Hello, traveler!"
        self.image = image if image else pygame.Surface((40, 60))  # Default placeholder size for NPC
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def interact(self):
        """Trigger an NPC interaction, such as displaying dialogue."""
        print(f"{self.name}: {self.dialogue}")

    def update(self):
        """Any logic for updating NPC's state could go here."""
        pass

#loads in npcs as a dictionary
def load_npcs():
    with open("data/npcs.json", "r") as f:
        data = json.load(f)
    
    npc_dict = {}
    for npc_name, npc_data in data.items():
        npc = NPC(
            name=npc_data["name"],
            x=npc_data["x"],
            y=npc_data["y"],
            dialogue=npc_data["dialogue"]
        )
        npc_dict[npc_name] = npc
    return npc_dict