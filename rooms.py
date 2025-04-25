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
        if isinstance(self.background, pygame.Surface):  # if background is an image
            screen.blit(self.background, (0, 0))
        else:  # If background is a color
            screen.fill(self.background)
        for npc in self.npcs:
            npc.draw(screen)


    def update(self, player, room_manager):
         # east aka right
        if player.rect.right >= settings.SCREEN_WIDTH and "east" in self.exits:
            self.next_room = self.exits["east"]
            return "east"
        # west aka left
        elif player.rect.left <= 0 and "west" in self.exits:
            self.next_room = self.exits["west"]
            return "west"
        # north aka top
        elif player.rect.top <= 0 and "north" in self.exits:
            self.next_room = self.exits["north"]
            return "south"
        # south aka bottom
        elif player.rect.bottom >= settings.SCREEN_HEIGHT and "south" in self.exits:
            self.next_room = self.exits["south"]
            return "north"
        else:
            self.next_room = None  # stay in current room



class RoomManager:
    def __init__(self, rooms, start_room):
        self.rooms = rooms  # dictionary containing the rooms
        self.current_room = self.rooms[start_room] # current room

    # switches to another room
    def switch_room(self, new_room_name):
        if new_room_name in self.rooms:
            self.current_room = self.rooms[new_room_name]
            pygame.display.set_caption(self.current_room.name)
        else:
            print(f"Room '{new_room_name}' not found.")

    # determines if the player has entered another room
    def update(self, player, text_box, hud):
        for npc in self.current_room.npcs:
            npc.wander(player)
        direction = self.current_room.update(player, self)
        if self.current_room.next_room:
            text_box.hide()
            hud.room = self.current_room.next_room # changes the name on the hud
            player.reset_position(direction)
            self.switch_room(self.current_room.next_room)

    # draws the room
    def draw(self, screen):
        self.current_room.draw(screen)


# loads in the rooms from the json
def load_rooms(npc_list):
    with open('data/rooms.json', 'r') as file:
        rooms_data = json.load(file)

    # dictionary that holds all the room information
    rooms = {}
    for room_name, room_info in rooms_data.items():
        background = pygame.image.load(room_info['background'])
        exits = room_info['exits']

        # gets the npcs in the room
        npc_names = room_info.get("npcs", [])
        npcs_in_room = [npc_list[name] for name in npc_names if name in npc_list]
        
        # sets up the room
        room = Room(
            room_info['name'], 
            room_info['description'], 
            background, 
            exits,
            npcs_in_room
        )
        # adds the room
        rooms[room_name] = room


    return rooms

