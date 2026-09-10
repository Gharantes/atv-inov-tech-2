# Serviço de IA — por enquanto usa respostas mock.
# Quando a integração com a API de IA for feita, basta trocar a implementação
# de `generate_reply` por uma chamada ao modelo, mantendo a mesma assinatura.

import random
import re

from app.schemas import ChatMessage

MOCK_RESPONSES = [
    {
        "keywords": ["olá", "ola", "oi", "bom dia", "boa tarde", "boa noite"],
        "reply": "Olá! 👋 Sou um assistente virtual. Como posso ajudar você hoje?",
    },
    {
        "keywords": ["react"],
        "reply": (
            "React é uma biblioteca JavaScript para construir interfaces de usuário. Ela trabalha "
            "com componentes reutilizáveis e um DOM virtual, o que torna a atualização da tela eficiente."
        ),
    },
    {
        "keywords": ["python", "fastapi"],
        "reply": (
            "FastAPI é um framework Python moderno para criar APIs. Ele é rápido, usa type hints "
            "para validação automática e gera documentação interativa em /docs."
        ),
    },
    {
        "keywords": ["ia", "inteligência artificial", "inteligencia artificial"],
        "reply": (
            "Inteligência Artificial é a área da computação que busca criar sistemas capazes de "
            "realizar tarefas que normalmente exigem inteligência humana, como entender linguagem, "
            "reconhecer imagens e tomar decisões."
        ),
    },
    {
        "keywords": ["piada"],
        "reply": "Por que o programador foi ao médico? Porque ele estava com muitos *bugs*! 🐛",
    },
    {
        "keywords": ["obrigado", "obrigada", "valeu"],
        "reply": "Por nada! Se tiver mais alguma dúvida, é só perguntar. 😊",
    },
]

FALLBACK_REPLIES = [
    "Interessante! Ainda estou em modo de demonstração, mas em breve poderei responder isso usando uma IA de verdade.",
    "Boa pergunta! No momento estou usando respostas simuladas enquanto a API de IA não é integrada.",
    "Entendi sua mensagem. Quando a integração com a API de IA estiver concluída, darei uma resposta mais completa.",
]


def contains_word(text: str, keyword: str) -> bool:
    """Verifica se a palavra-chave aparece como palavra inteira (evita "ia" casar com "piada")."""
    return re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", text) is not None


def find_mock_reply(message: str) -> str:
    text = message.lower()
    for response in MOCK_RESPONSES:
        if any(contains_word(text, keyword) for keyword in response["keywords"]):
            return response["reply"]
    return random.choice(FALLBACK_REPLIES)


async def generate_reply(message: str, history: list[ChatMessage]) -> str:
    """Gera a resposta da IA para a mensagem do usuário.

    `history` contém as mensagens anteriores da conversa; ainda não é usado pelo
    mock, mas será enviado ao modelo de IA como contexto.
    """
    return find_mock_reply(message)
