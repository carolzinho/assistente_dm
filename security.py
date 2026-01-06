import re
import time
from collections import defaultdict

REQUEST_LIMIT = 10      # máx. mensagens
WINDOW_SECONDS = 60     # por minuto

_user_requests = defaultdict(list)


def check_rate_limit(user_id: str) -> bool:
    """
    Retorna False se o usuário exceder o limite
    """
    now = time.time()
    window_start = now - WINDOW_SECONDS

    requests = [
        t for t in _user_requests[user_id]
        if t > window_start
    ]

    requests.append(now)
    _user_requests[user_id] = requests

    return len(requests) <= REQUEST_LIMIT


def sanitize_input(text: str) -> str:
    if not text:
        return ""

    text = text[:300]
    
    text = re.sub(r"[<>$`{}]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_forbidden_content(text: str) -> bool:
    forbidden_patterns = [
        r"rm\s+-rf",
        r"os\.system",
        r"subprocess",
        r"import\s+os",
        r"drop\s+table",
        r"delete\s+from",
        r"shutdown",
    ]

    text = text.lower()

    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            return True

    return False
