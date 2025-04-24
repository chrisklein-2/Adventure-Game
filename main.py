import pygame
import settings
import sys
from player import Player
import rooms as rm
import npcs
from textbox import TextBox
import quests
import dialogueManager
from hud import HUD
# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
text_box = TextBox(760, 100)  # display text, slightly smaller than full width
text_box.show("Use the arrow keys or WASD to move! Press E to interact!")
font = pygame.font.Font(None, 36)  # font for text rendering
pygame.display.set_caption("Adventure Game")
hud = HUD()

# set up clock
clock = pygame.time.Clock()

def game_loop():
    intro_message = True
    print("Make quest objectives, fix hud box to fit desc")
    player = Player(400, 300, settings.PLAYER_SPEED)

    # main game loop
    running = True
    
    npc_list = npcs.load_npcs()    
    rooms = rm.load_rooms(npc_list)  
    room_manager = rm.RoomManager(rooms, settings.StarterRoom)
    pygame.display.set_caption("Town Square")

    quest_manager = quests.QuestManager(quests.load_quests())
    dialogue_manager = dialogueManager.DialogueManager()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if intro_message:
                    text_box.hide()
                    intro_message = False
                if dialogue_manager.active:
                    player.can_move=False
                    if event.key == pygame.K_e:
                        dialogue_manager.advance(text_box, player, hud)
                else:
                    player.handle_interaction(event, room_manager.current_room.npcs, text_box, quest_manager, dialogue_manager, hud)

        # handle input
        keys = pygame.key.get_pressed()
        player.update(keys, hud, room_manager.current_room.npcs)


        # update
        room_manager.update(player, text_box, hud)
        
        if keys[pygame.K_q]:
            text_box.hide()
        
        # draw
        screen.fill(settings.WHITE)
        room_manager.draw(screen)
        player.draw(screen)
        text_box.draw(screen)
        hud.draw(screen)

        pygame.display.flip()

        clock.tick(settings.FPS)


game_loop()
pygame.quit()
sys.exit()