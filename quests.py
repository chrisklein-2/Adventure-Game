import json

class QuestManager:
    def __init__(self, quest_data):
        self.quests = quest_data

    # checks if quest is still ongoing
    def is_quest_active(self, quest_id):
        quest = self.quests.get(quest_id)
        if quest and not quest["completed"]:
            return True
        else:
            return False

    # returns the npc needed to talk to for the next quest step
    def get_current_npc(self, quest_id):
        quest = self.quests.get(quest_id)
        if quest:
            step = quest["steps"][quest["current_step"]]
            return step["npc"]
        return None

    # moves onto next step if you're talking to correct npc
    def next_quest_step(self, quest_id, hud):
        quest = self.quests.get(quest_id)
        if quest:
            quest["current_step"] += 1
            if quest["current_step"] >= len(quest["steps"]):
                quest["completed"] = True
            if quest["current_step"] < len(quest["steps"]):
                hud.questObj = quest["steps"][quest["current_step"]]["objective"]

    # adds beginning and end line
    # sets up hud for quest
    def set_up_quest(self, quest_id, hud):
        start = {"speaker":"start", "line": f"You've began the {self.quests[quest_id]["name"]} quest!"}
        self.quests[quest_id]["steps"][0]["dialogue"].insert(0,start)
        start = {"speaker":"end", "line": f"You've completed {self.quests[quest_id]["name"]}!"}
        self.quests[quest_id]["steps"][-1]["dialogue"].append(start)
        
        hud.quest = self.quests[quest_id]["name"]
        hud.questObj = self.quests[quest_id]["steps"][0]["objective"]

    def advance_quest(self, quest_id, text_box, hud, player, npc, dialogue_manager):
        # checks if npc is next to talk to and that the quest is active
        quest = self.get_current_quest(quest_id)

        # initializes quest and hud
        if quest["current_step"]==0:
            self.set_up_quest(quest_id, hud)
            
        # finds where the player is in quest then gets the dialogue associated with it
        stepNum = quest["current_step"]
        current_step = quest["steps"][stepNum]

        # after dialogue starts it is taken care of in the main loop
        # this is for one set of dialogue, so one conversation
        dialogue_manager.start_dialogue(npc, current_step["dialogue"])
        dialogue_manager.advance(text_box, player, hud)
        self.next_quest_step(quest_id, hud)

        if quest["completed"]==True:
            player.inventory.append(quest["reward"])


    def get_current_quest(self, quest_id):
        return self.quests[quest_id]

def load_quests():
    with open('data/quests.json', 'r') as file:
        quest_data = json.load(file)
    return quest_data