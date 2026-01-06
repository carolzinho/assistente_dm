from agenda import get_available_slots, is_slot_available
from datetime import datetime, timedelta
import re

def validate_date(data: str) -> bool:
    if not data:
        return False

    slots = get_available_slots(data)
    return bool(slots)


def validate_time(data: str, horario: str) -> bool:
    if not data or not horario:
        return False

    return is_slot_available(data, horario)


from datetime import datetime, timedelta
import re

VALID_SPECIALTIES = {
    "cardiologista": ["cardio", "cardiologia"],
    "dermatologista": ["dermato", "pele"],
    "ortopedista": ["ortopedia", "osso"],
    "clinico geral": ["clinico", "geral"]
}

def normalize_specialty(text: str) -> str | None:
    text = text.lower().strip()

    for official, aliases in VALID_SPECIALTIES.items():
        if text == official or text in aliases:
            return official

    return None


def parse_date(text: str) -> str | None:
    text = text.lower().strip()
    today = datetime.today().date()

    if text == "hoje":
        return today.isoformat()

    if text == "amanhã" or text == "amanha":
        return (today + timedelta(days=1)).isoformat()

    try:
        date = datetime.strptime(text, "%Y-%m-%d").date()
        if date < today:
            return None
        return date.isoformat()
    except ValueError:
        return None


def parse_time(text: str, date_iso: str | None) -> str | None:
    match = re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", text)
    if not match:
        return None

    hour, minute = map(int, text.split(":"))

    if hour < 8 or hour > 18:
        return None

    if date_iso:
        date = datetime.fromisoformat(date_iso).date()
        now = datetime.now()

        if date == now.date():
            time_obj = datetime.strptime(text, "%H:%M").time()
            if time_obj <= now.time():
                return None

    return text
