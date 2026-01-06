
class ConversationState:
    def __init__(self):
        self.intent = None
        self.data = {
            "especialidade": None,
            "medico": None,
            "data": None,
            "horario": None
        }

    def is_complete(self):
        return all(self.data.values())

    def next_missing_field(self):
        for key, value in self.data.items():
            if value is None:
                return key
        return None
