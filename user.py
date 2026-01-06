import uuid


def generate_user_id() -> str:
    """
    id unico por user (jwt depois)
    """
    return str(uuid.uuid4())
