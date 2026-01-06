from llm import call_llm
from prompts import SYSTEM_PROMPT_CLINICA, TRIAGE_PROMPT
from cache import load_session, save_session


def classify_intent(message: str) -> str:
    prompt = TRIAGE_PROMPT.format(message=message)
    response = call_llm(prompt)
    return response.strip()


def handle_message(user_id: str, message: str) -> str:
    history = load_session(user_id)

    category = classify_intent(message)

    if category == "POSSIVEL_URGENCIA":
        response = (
            "⚠️ Entendi sua mensagem e ela pode indicar uma situação de urgência.\n\n"
            "Por favor, procure imediatamente um pronto atendimento ou ligue para o SAMU (192)."
        )

    elif category == "AGENDAMENTO":
        response = (
            "Claro 😊 Posso te ajudar com o agendamento.\n\n"
            "Você poderia me informar a especialidade desejada "
            "e se o atendimento será particular ou por convênio?"
        )

    elif category == "VALORES":
        response = (
            "Os valores podem variar de acordo com a especialidade e o tipo de atendimento.\n\n"
            "Você poderia me informar qual consulta deseja realizar?"
        )

    elif category == "CONVENIO":
        response = (
            "Atendemos diversos convênios 😊\n\n"
            "Poderia me informar qual convênio você possui?"
        )

    else:
        response = (
            "Olá! 😊 Como posso te ajudar hoje?"
        )

    history.append({
        "user": message,
        "assistant": response
    })

    save_session(user_id, history)

    return response
