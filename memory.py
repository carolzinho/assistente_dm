from typing import Dict
from db import (
    init_db,
    get_conversation_db,
    save_conversation_db,
    delete_conversation_db
)


init_db()


DEFAULT_STATE = {
    "intent": None,
    "urgency": "normal",
    "especialidade": None,
    "medico": None,
    "data": None,
    "horario": None,
    "last_question": None,
    "stage": "inicio",
}


def get_conversation(user_id: str) -> Dict:
    convo = get_conversation_db(user_id)

    if convo is None:
        convo = DEFAULT_STATE.copy()
        save_conversation_db(user_id, convo)

    return convo


def update_conversation(user_id: str, updates: Dict):
    convo = get_conversation(user_id)
    convo.update(updates)
    save_conversation_db(user_id, convo)


def reset_conversation(user_id: str):
    delete_conversation_db(user_id)
