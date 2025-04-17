import pygame
import settings
import sys
from player import Player
import rooms as rm
import npcs

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
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
    rooms = rm.load_rooms()  # Load the rooms from the JSON file
    room_manager = rm.RoomManager(rooms, 'forest')
    pygame.display.set_caption("The Forest")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #handle input
        keys = pygame.key.get_pressed()
        player.update(keys, npc)

        #update
        room_manager.update(player)
        
        #draw
        screen.fill(settings.WHITE)
        room_manager.draw(screen)
        player.draw(screen)

        pygame.display.flip()

        
        clock.tick(settings.FPS)


game_loop()
pygame.quit()
sys.exit()