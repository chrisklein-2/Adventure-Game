import json

def add_room_to_file(file_path, room_id, room_data):
    try:
        # Load existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file is empty or doesn't exist, initialize as an empty dict
        data = {}

    # Add new NPC under a unique key
    data[room_id] = room_data

    # Save updated dictionary back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# the room name is the ID, so they will be the same
# the exits can be kept null unless you know where they will be connected to, just make sure to update the connection

room_name = "Secret Tunnel"
new_room = {
      "name": "Secret Tunnel",
        "description": "Through the mountain",
        "background": "assets/images/secretTunnel.jpg",
        "music": "assets/sounds/secretTunnel.wav",
        "exits": {
            "north": None,
            "east": None,
            "west": None,
            "south": None
        },
        "npcs": []
}

add_room_to_file('data/rooms.json', room_name, new_room)