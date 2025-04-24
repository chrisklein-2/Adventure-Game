import pygame
import settings

class HUD:

    def __init__(self):
        self.width = 300
        self.height = 100
        self.font = pygame.font.Font(None, 26)
        self.left = settings.SCREEN_WIDTH-self.width

        self.hud_rect = pygame.Rect(self.left, 0, self.width, self.height)

        self.padding = 10
        self.text_color = settings.BLACK
        self.hud_color = (240, 240, 240)
        self.room = settings.StarterRoom
        self.quest = None
        self.questObj = None

    def draw(self, screen):

        pygame.draw.rect(screen, self.hud_color, self.hud_rect)
        pygame.draw.rect(screen, settings.BLACK, self.hud_rect, 2)  # border

        # adds a text that displays the current room
        text = "Room: " + self.room.title()
        text_surface = self.font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.hud_rect.x + self.padding, self.hud_rect.y + self.padding))

        # adds quest title and object to hud if active
        if self.quest:
            text = "Quest: " + self.quest.title()
            text_surface = self.font.render(text, True, self.text_color)
            screen.blit(text_surface, (self.hud_rect.x + self.padding, self.hud_rect.y + self.padding + 25))

            # wraps description if too long            
            text = "Next objective: " + self.questObj
            wrapped_lines = self.wrap_text(text, self.font, self.width - 2 * self.padding)

            # prints quest objective and changes textbox size if needed
            for i, line in enumerate(wrapped_lines):

                text_surface = self.font.render(line, True, self.text_color)   
                self.update_height(i*25)

                screen.blit(text_surface, (self.hud_rect.x + self.padding, self.hud_rect.y + self.padding + 50 + i*25))


    # increases/decreases height of hud, resets if the value is empty or 0
    def update_height(self, height_change=0):
        if height_change == 0:
            self.hud_rect.height = self.height
        self.hud_rect.height += height_change

    # setting up the wrapped text
    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        return lines
