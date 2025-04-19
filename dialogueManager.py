class DialogueManager:
    def __init__(self):
        self.active = False
        self.dialogue_lines = []
        self.current_line = 0
        self.npc_name = ""
        self.npc = None
    
    #begins the dialogue then keeps it active until its through
    def start_dialogue(self, npc, lines):
        self.dialogue_lines = lines
        self.current_line = 0
        self.active = True
        self.npc_name = npc.name
        self.npc = npc
        npc.speed = 0
    
    #keeps dialogue going waiting for the next line
    def advance(self, text_box, player):
        if self.current_line < len(self.dialogue_lines):
            line = self.dialogue_lines[self.current_line]
            speaker = "" 
            if line["speaker"] == "player":
                 speaker = "You say :"
            elif line["speaker"] == "npc": 
                speaker = self.npc_name + " says:"
            else:
                speaker = ""
            text_box.show(f"{speaker} {line['line']}")
            self.current_line += 1
        else:
            player.can_move = True
            self.end(text_box)
    
    #ends dialogue
    def end(self, text_box):
        text_box.hide()
        self.active = False
        self.npc.speed = 1
