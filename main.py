import pygame
import settings
import sys
from player import Player
import rooms as rm
import npcs
from textbox import TextBox


# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
text_box = TextBox(760, 100)  # slightly smaller than full width
font = pygame.font.Font(None, 36)  # Font for text rendering
pygame.display.set_caption("Adventure Game")

# Set up clock
clock = pygame.time.Clock()

def game_loop():

    player = Player(400, 300, 5)

    # Main game loop
    running = True
    npc = pygame.Rect(300, 100, 20, 20)  # NPC position (just a rectangle for this example)
    
    npc_list = npcs.load_npcs()    
    rooms = rm.load_rooms(npc_list)  # Load the rooms from the JSON file
    room_manager = rm.RoomManager(rooms, 'forest')
    pygame.display.set_caption("The Forest")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #handle input
        keys = pygame.key.get_pressed()
        player.update(keys, text_box, room_manager.current_room.npcs)

        #update
        room_manager.update(player)
        
        if keys[pygame.K_q]:
            text_box.hide()
        
        #draw
        screen.fill(settings.WHITE)
        room_manager.draw(screen)
        player.draw(screen)
        text_box.draw(screen)

        pygame.display.flip()

        
        clock.tick(settings.FPS)


game_loop()
pygame.quit()
sys.exit()