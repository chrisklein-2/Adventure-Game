import json
class QuestManager:
    def __init__(self, quest_data):
        self.quests = quest_data

    #checks if quest is still ongoing
    def is_quest_active(self, quest_id):
        quest = self.quests.get(quest_id)
        if quest and not quest["completed"]:
            return True
        else:
            return False

    #returns the npc needed to talk to for the next quest step
    def get_current_npc(self, quest_id):
        quest = self.quests.get(quest_id)
        if quest:
            step = quest["steps"][quest["current_step"]]
            return step["npc"]
        return None

    #moves onto next step if you're talking to correct npc
    def advance_quest(self, quest_id):
        quest = self.quests.get(quest_id)
        if quest:
            quest["current_step"] += 1
            if quest["current_step"] >= len(quest["steps"]):
                quest["completed"] = True

    def quest_dialogue(self, dialogue, text_box, npc):
        
        for line in dialogue:
            text_box.show(f"{npc.name} says: {line}")


def load_quests():
    with open('data/quests.json', 'r') as file:
        quest_data = json.load(file)
    return quest_data