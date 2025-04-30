import settings
import pygame
import json

class GameObject:

    def __init__(self, x, y, width, height, solid):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.solid = solid
        self.color = settings.WHITE
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.obj_rect)

    def update(self, screen):
        self.draw(screen)


# loads in objects as a dictionary
def load_objects():
    with open("data/objects.json", "r") as f:
        data = json.load(f)
    
    obj_dict = {}
    for obj_name, obj_data in data.items():
        obj = GameObject(
            x = obj_data["x"],
            y = obj_data["y"],
            width = obj_data["width"],
            height = obj_data["height"],
            solid = obj_data["solid"]
        )
        obj_dict[obj_name] = obj
    return obj_dict