import pygame
import settings

# Player class
class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(x, y, 32, 50)  # rectangle for collision detection
        self.color = settings.BLUE # the players color
        self.attack_width = 15
        self.attack_box = pygame.Rect(x-self.attack_width, y, self.attack_width, 50)
        self.can_move = True
        self.inventory = []
        self.walk_sound = pygame.mixer.Sound("assets/sounds/walking.wav")
        self.direction = "right" # which way are they facing
        
    def update(self, keys, hud, npcs=None):
        self.handle_movement(keys, hud, npcs)


    # lets the player move around with arrow keys
    def handle_movement(self, keys, hud, npcs):
        if not self.can_move:
            return
        prev_x, prev_y = self.x, self.y
        dx, dy = 0, 0 # the difference in the movements
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x > 0:
                dx -= self.speed
                self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.x < settings.SCREEN_WIDTH - self.rect.width:
                dx += self.speed
                self.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.y > 0:
                dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.y < settings.SCREEN_HEIGHT - self.rect.height:
                dy += self.speed
        
        new_rect = self.rect.move(dx, dy)
        # collision detection for npcs
        if not any(new_rect.colliderect(npc.rect) for npc in npcs):
            # update player's position after moving
            self.x += dx
            self.y += dy
            self.rect.x = self.x
            self.rect.y = self.y

            # moves attack box with player
            if self.direction == "left":
                self.attack_box.topleft = (self.rect.x - self.attack_width, self.rect.y)
            elif self.direction == "right":
                self.attack_box.topleft = (self.rect.x + self.rect.width, self.rect.y)
            if self.x != prev_x or self.y != prev_y:
                if not self.walk_sound.get_num_channels():
                    self.walk_sound.play()

        # collison detection for the hud
        if new_rect.colliderect(hud.hud_rect):
            if hud.hud_rect.left == 0:
                hud.hud_rect.left = settings.SCREEN_WIDTH-hud.width
            else:
                hud.hud_rect.left = 0

    # draws the player
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, settings.BLACK, self.attack_box)

    # handles interactions with npcs
    def handle_interaction(self, event, npcs, text_box, quest_manager, dialogue_manager, hud):

        # buffer zone for interacting with npcs
        buffer = 50
        buffer_rect = self.rect.inflate(buffer, buffer)
        
        if event.key == pygame.K_e:
            # cycles through all the npcs in the room
            for npc in npcs:
                if buffer_rect.colliderect(npc.rect):

                    # checks if the npc is in any quest
                    for quest_id in quest_manager.quests:

                        # checks if npc is next to talk to and that the quest is active
                        if quest_manager.is_quest_active(quest_id) and npc.name == quest_manager.get_current_npc(quest_id):
                            quest = quest_manager.get_current_quest(quest_id)

                            # initializes quest and hud
                            if quest["current_step"]==0:
                                quest_manager.set_up_quest(quest_id)
                                hud.quest = quest["name"]
                                hud.questObj = quest["steps"][0]["objective"]
                        
                            # finds where the player is in quest then gets the dialogue associated with it
                            stepNum = quest["current_step"]
                            current_step = quest["steps"][stepNum]

                            dialogue_manager.start_dialogue(npc, current_step["dialogue"])
                            dialogue_manager.advance(text_box, self, hud)
                            quest_manager.advance_quest(quest_id, hud)

                            if quest["completed"]==True:
                                self.inventory.append(quest["reward"])
                            return
                    
                    # if it isn't then it just says its dialogue
                    line = npc.check_next_line()
                    
                    if line:
                        npc.interact(text_box)
                    else:
                        text_box.hide()
                        npc.reset_dialogue()
                        npc.interact(text_box)
                    break

    # moves player to appropriate position after changing rooms
    def reset_position(self, direction=None):
        if direction == "south":
            self.y = settings.SCREEN_HEIGHT - 20
        elif direction == "north":
            self.y = 0
        elif direction == "east":
            self.x = 0
        elif direction == "west":
            self.x = settings.SCREEN_WIDTH - 20
        else:
            self.rect.x, self.rect.y = settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2
