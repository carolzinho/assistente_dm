import json
import os

CACHE_DIR = "sessions"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def load_session(user_id: str):
    path = os.path.join(CACHE_DIR, f"{user_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_session(user_id: str, history):
    path = os.path.join(CACHE_DIR, f"{user_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
