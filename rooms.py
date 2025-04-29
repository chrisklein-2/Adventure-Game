import pygame
import json
import settings

class Room:
    def __init__(self, name, description, background, music, exits, npcs=None, objects=None):
        self.name = name  
        self.description = description  
        self.background = background  
        self.music = music
        self.exits = exits  
        self.npcs = npcs if npcs else []  
        self.objects = objects if objects else [] # not implemented yet
        self.next_room = None

    def draw(self, screen):
        # draw background image or color
        if isinstance(self.background, pygame.Surface):  # if background is an image
            screen.blit(self.background, (0, 0))
        else:  # if background is a default color
            screen.fill(self.background)
        for npc in self.npcs:
            npc.draw(screen)
        for obj in self.objects:
            obj.draw(screen)


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
        self.current_music = None

    # switches to another room
    def switch_room(self, new_room_name):
        if new_room_name in self.rooms:
            self.current_room = self.rooms[new_room_name]
            pygame.display.set_caption(self.current_room.name)
        else:
            print(f"Room '{new_room_name}' not found.")

    def set_music(self, music_track):

        if self.current_music != music_track:

            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            if self.current_room.music:  # make sure a path is provided
                pygame.mixer.music.load(self.current_room.music)
                pygame.mixer.music.set_volume(.08)
                pygame.mixer.music.play(-1)
            self.current_music = music_track

    # determines if the player has entered another room
    def update(self, player, text_box, hud):
        for npc in self.current_room.npcs:
            npc.wander(player)
        direction = self.current_room.update(player, self)

        if not pygame.mixer.music.get_busy():
            self.set_music(self.current_room.music)

        if self.current_room.next_room:
            text_box.hide() #gets rid of the text box if still open
            hud.room = self.current_room.next_room # changes the name on the hud
            player.reset_position(direction)
            old_music = self.current_room.music

            #switches to the next room
            self.switch_room(self.current_room.next_room)

            self.set_music(self.current_room.music)
            
                        
    # draws the room
    def draw(self, screen):
        self.current_room.draw(screen)


# loads in the rooms from the json
def load_rooms(npc_list, obj_list):
    with open('data/rooms.json', 'r') as file:
        rooms_data = json.load(file)

    # dictionary that holds all the room information
    rooms = {}
    for room_name, room_info in rooms_data.items():
        background = pygame.image.load(room_info['background'])
        music = room_info["music"]
        exits = room_info['exits']

        # gets the npcs in the room
        npc_names = room_info.get("npcs", [])
        obj_names = room_info.get("objects", [])
        npcs_in_room = [npc_list[name] for name in npc_names if name in npc_list]
        objs_in_room = [obj_list[name] for name in obj_names if name in obj_list]
        # sets up the room
        room = Room(
            room_info['name'], 
            room_info['description'], 
            background, 
            music,
            exits,
            npcs_in_room,
            objs_in_room
        )
        # adds the room
        rooms[room_name] = room


    return rooms

