import pygame
import json
import settings

class Room:
    def __init__(self, name, description, background, exits, npcs=None, objects=None):
        self.name = name  # Name of the room (e.g., "Library")
        self.description = description  # The text description of the room
        self.background = background  # Background image or color (could be a string or pygame.Surface)
        self.exits = exits  # A dictionary of possible exits {north: "Room Name", east: "Room Name", etc.}
        self.npcs = npcs if npcs else []  # List of NPCs in the room (could be NPC objects)
        self.objects = objects if objects else []  # List of objects that are interactable (could be items or other objects)
        self.next_room = None

    def draw(self, screen):
        # Draw background image or color
        if isinstance(self.background, pygame.Surface):  # If background is a pygame surface (image)
            screen.blit(self.background, (0, 0))
        else:  # If background is a color
            screen.fill(self.background)


    def update(self, player, room_manager):
         # Right edge (east)
        if player.rect.right >= settings.SCREEN_WIDTH and "east" in self.exits:
            self.next_room = self.exits["east"]
            return "east"
        # Left edge (west)
        elif player.rect.left <= 0 and "west" in self.exits:
            self.next_room = self.exits["west"]
            return "west"
        # Top edge (north)
        elif player.rect.top <= 0 and "north" in self.exits:
            self.next_room = self.exits["north"]
            return "south"
        # Bottom edge (south)
        elif player.rect.bottom >= settings.SCREEN_HEIGHT and "south" in self.exits:
            self.next_room = self.exits["south"]
            return "north"
        else:
            self.next_room = None  # Stay in current room



class RoomManager:
    def __init__(self, rooms, start_room):
        self.rooms = rooms  # Dictionary of room_name: Room instance
        self.current_room = self.rooms[start_room]


    def switch_room(self, new_room_name):
        if new_room_name in self.rooms:
            self.current_room = self.rooms[new_room_name]
            pygame.display.set_caption(self.current_room.name)
        else:
            print(f"Room '{new_room_name}' not found.")

    def update(self, player):
        direction = self.current_room.update(player, self)
        if self.current_room.next_room:
            player.reset_position(direction)
            self.switch_room(self.current_room.next_room)

    def draw(self, screen):
        self.current_room.draw(screen)


def load_rooms():
    with open('data/rooms.json', 'r') as file:
        rooms_data = json.load(file)

    rooms = {}
    for room_name, room_info in rooms_data.items():
        background = pygame.image.load(room_info['background'])
        exits = room_info['exits']
        room = Room(room_info['name'], room_info['description'], background, exits)
        rooms[room_name] = room
    return rooms

