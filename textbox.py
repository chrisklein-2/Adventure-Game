import pygame
import settings

class TextBox:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 28)
        self.text = ""
        self.visible = False

        self.box_rect = pygame.Rect(20, settings.SCREEN_HEIGHT - height - 20, width, height)
        self.padding = 10
        self.text_color = settings.BLACK
        self.box_color = (240, 240, 240)

    #shows the textbox when interaction starts
    def show(self, text):
        self.text = text
        self.visible = True

    #hides the textbox
    def hide(self):
        self.visible = False

    def draw(self, screen):
        #sets up textbox if it isnt hidden
        if self.visible:
            pygame.draw.rect(screen, self.box_color, self.box_rect)
            pygame.draw.rect(screen, settings.BLACK, self.box_rect, 2)  # border

            wrapped_lines = self.wrap_text(self.text, self.font, self.width - 2 * self.padding)
            for i, line in enumerate(wrapped_lines):
                text_surface = self.font.render(line, True, self.text_color)
                screen.blit(text_surface, (self.box_rect.x + self.padding, self.box_rect.y + self.padding + i * 24))

    #adds the words to the textbox
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
        lines.append("")
        lines.append("Press q to close screen...")
        return lines
