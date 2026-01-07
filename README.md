Assistente conversacional inteligente para **agendamento de consultas médicas**, com foco em **fluxo conversacional robusto**, validação de dados e arquitetura extensível.

Projeto desenvolvido em Python, com separação clara de responsabilidades, pronto para evoluir para integrações externas (WhatsApp, API REST, RAG, etc).

---

O modelo:
- Conduz conversas naturais
- Coleta dados de forma incremental
- Valida informações críticas (data, horário, especialidade)
- Lida com erros e ambiguidades do usuário
- Confirma agendamentos de forma segura


---

## Principais Funcionalidades

- Classificação de intenção e urgência
- Extração de entidades (especialidade, data, horário, médico)
- Gerenciamento de estado conversacional
- Validação robusta de dados
- Detecção de emergências médicas
- Simulação de agenda e reserva de horários
- Confirmação inteligente de agendamento
- Arquitetura preparada para RAG e APIs externas

## Stack

- Python 3.10
- Google Gemini (LLM)

---

## COMO USAR:

Este projeto utiliza a API do Google Gemini. Configure o ambiente para rodar localmente:

1. Crie uma chave de API no Google AI Studio: https://aistudio.google.com/app/apikey
2. Crie um arquivo `.env` na raiz do projeto
3. Adicione sua chave no seguinte formato:

```env
GOOGLE_API_KEY=SUACHAVEAQUI

Instalar e realizar a execução local do arquivo via terminal:

```bash
python router.py
