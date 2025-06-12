import json
import os

SAVE_FILE = "save_data.json"

def save_game_state(player_id):
    data = {"player_id": player_id}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("💾 Game state saved.")

def load_game_state():
    if not os.path.exists(SAVE_FILE):
        return None

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("player_id")
    except Exception as e:
        print(f"⚠️ Failed to load save data: {e}")
        return None

def clear_game_state():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
