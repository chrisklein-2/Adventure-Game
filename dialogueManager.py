class DialogueManager:
    def __init__(self):
        self.active = False
        self.dialogue_lines = []
        self.current_line = 0
        self.npc_name = ""
    
    #begins the dialogue then keeps it active until its through
    def start_dialogue(self, npc_name, lines):
        self.dialogue_lines = lines
        self.current_line = 0
        self.active = True
        self.npc_name = npc_name
    
    #keeps dialogue going waiting for the next line
    def advance(self, text_box):
        if self.current_line < len(self.dialogue_lines):
            text_box.show(f"{self.npc_name} says: {self.dialogue_lines[self.current_line]}")
            self.current_line += 1
        else:
            self.end(text_box)
    
    #ends dialogue
    def end(self, text_box):
        text_box.hide()
        self.active = False
