from typing import Dict, List

#agenda simulada 
_agenda: Dict[str, List[str]] = {
    "2025-01-10": ["09:00", "10:00", "14:00", "15:00", "16:00"],
    "2025-01-11": ["09:00", "11:00", "13:00", "15:00"],
}


def normalize_date(date_str: str) -> str:
    """
    Normaliza datas simples como 'amanhã' ou 'hoje'
    (por enquanto hardcoded)
    """
    if date_str.lower() == "amanhã":
        return "2025-01-10"
    if date_str.lower() == "hoje":
        return "2025-01-09"
    return date_str


def get_available_slots(date: str) -> List[str]:
    date = normalize_date(date)
    return _agenda.get(date, [])


def is_slot_available(date: str, time: str) -> bool:
    date = normalize_date(date)
    return time in _agenda.get(date, [])


def reserve_slot(date: str, time: str) -> bool:
    date = normalize_date(date)

    if date in _agenda and time in _agenda[date]:
        _agenda[date].remove(time)
        return True

    return False
