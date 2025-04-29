import json

def add_npc_to_file(file_path, npc_id, new_npc_data):
    try:
        # Load existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file is empty or doesn't exist, initialize as an empty dict
        data = {}

    # Add new NPC under a unique key
    data[npc_id] = new_npc_data

    # Save updated dictionary back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
npc_name = "Bob Sacamano"
new_npc = {
      "name": "Bob Sacamano",
      "x": 200,
      "y": 490,
      "image": "assets/images/alpha/letterT.png",
      "dialogue": ["Have you seen Kramer?", "I've got a great plan to get rich!"]
}

add_npc_to_file('data/npcs.json', npc_name, new_npc)