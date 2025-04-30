import pygame
import settings
from gameObject import GameObject

def set_music(music_track):

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    if music_track:  # make sure a path is provided
        pygame.mixer.music.load(music_track)
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)

def switch_room(new_room_name, room_manager):
    room_manager.current_room = room_manager.rooms[new_room_name]
    pygame.display.set_caption(room_manager.current_room.description)


def force_switch_room(room_name, text_box, hud, room_manager, screen):
    text_box.hide() #gets rid of the text box if still open
    hud.room = room_manager.current_room.name
    
    #switches to the next room
    switch_room(room_name, room_manager)

    set_music(room_manager.rooms[room_name].music)