from agenda import get_available_slots, is_slot_available, reserve_slot
from intent import classify_intent
from entities import extract_entities
from memory import get_conversation, update_conversation, reset_conversation
from validators import normalize_specialty, parse_date, parse_time
from security import (
    sanitize_input,
    contains_forbidden_content,
    check_rate_limit
)
from user import generate_user_id
from dotenv import load_dotenv


load_dotenv()


def emergency_response():
    return (
        "⚠️ **Situação de emergência identificada**\n\n"
        "A falta de ar ou sintomas graves exigem atendimento imediato.\n\n"
        "**Por favor, ligue agora para o SAMU (192)** ou leve a pessoa ao "
        "pronto-socorro mais próximo."
    )



def next_question(user_id: str, conversation: dict) -> str | None:
    if not conversation.get("especialidade"):
        return "Qual **especialidade** você procura?"

    if not conversation.get("data"):
        return "Para qual **data** você deseja agendar? (YYYY-MM-DD, hoje ou amanhã)"

    if not conversation.get("horario"):
        return "Qual **horário** você prefere? (HH:MM)"

    update_conversation(user_id, {"stage": "confirmacao"})
    return None



def confirmation_message(conversation: dict) -> str:
    return (
        "Perfeito! 😊 Seguem os dados do agendamento:\n\n"
        f"• Especialidade: {conversation['especialidade']}\n"
        f"• Data: {conversation['data']}\n"
        f"• Horário: {conversation['horario']}\n\n"
        "Posso confirmar a consulta?"
    )



def route_message(user_id: str, user_input: str) -> str:

    # 🔐 Rate limit
    if not check_rate_limit(user_id):
        return "⚠️ Muitas mensagens em pouco tempo. Aguarde um momento, por favor."


    user_input = sanitize_input(user_input)

    if contains_forbidden_content(user_input):
        return "⚠️ Não posso processar esse tipo de solicitação."

    conversation = get_conversation(user_id)
    text = user_input.lower()

  
    intent_data = classify_intent(user_input)
    intent = intent_data["intent"]
    urgency = intent_data["urgency"]

    update_conversation(user_id, {
        "intent": intent,
        "urgency": urgency
    })

    
    if intent == "emergencia" or urgency == "alta":
        return emergency_response()

    
    if intent == "saudacao" and conversation["stage"] == "inicio":
        return "Olá! 😊 Como posso te ajudar hoje?"

    
    if intent == "marcar_consulta" and conversation["stage"] == "inicio":
        update_conversation(user_id, {"stage": "coletando_dados"})


    entities = extract_entities(user_input)
    updates = {}

    if entities.get("especialidade"):
        specialty = normalize_specialty(entities["especialidade"])
        if not specialty:
            return "Essa especialidade não está disponível 😕"
        updates["especialidade"] = specialty

    if entities.get("data"):
        date = parse_date(entities["data"])
        if not date:
            return "A data informada não é válida ou está no passado 😕"
        updates["data"] = date

    if entities.get("horario"):
        time = parse_time(entities["horario"], conversation.get("data"))
        if not time:
            return "Horário inválido 😕 Use HH:MM dentro do horário comercial."
        updates["horario"] = time

    if updates:
        update_conversation(user_id, updates)

    conversation = get_conversation(user_id)

    
    if conversation.get("data") and conversation.get("horario"):
        if not is_slot_available(conversation["data"], conversation["horario"]):
            slots = get_available_slots(conversation["data"])
            update_conversation(user_id, {"horario": None})

            if slots:
                return (
                    f"Esse horário não está disponível 😕\n\n"
                    f"Horários disponíveis para {conversation['data']}:\n"
                    + ", ".join(slots)
                )

            update_conversation(user_id, {"data": None})
            return "Esse dia não possui mais horários 😕 Deseja escolher outra data?"

    
    question = next_question(user_id, conversation)
    if question:
        return question

    return confirmation_message(conversation)



if __name__ == "__main__":
    USER_ID = generate_user_id()
    print(f"Usuário iniciado: {USER_ID}")

    while True:
        user_input = input("INPUT: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            reset_conversation(USER_ID)
            break

        output = route_message(USER_ID, user_input)
        print("\nOUTPUT:")
        print(output)
        print("-" * 50)
