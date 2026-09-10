# Serviço de IA — gera as respostas do chatbot usando a API do Google Gemini.
# A chave é lida da variável de ambiente GEMINI_API_KEY (veja backend/.env.example).

import logging
import os
from functools import cache

from google import genai
from google.genai import errors, types

from app.schemas import ChatMessage

logger = logging.getLogger(__name__)

# Modelos tentados em ordem: se o primeiro estiver sobrecarregado, usa o próximo
DEFAULT_MODELS = "gemini-flash-latest,gemini-flash-lite-latest"
TIMEOUT_MS = 25_000
# Erros temporários (limite de uso, sobrecarga) em que vale tentar o próximo modelo
RETRYABLE_STATUS_CODES = {429, 500, 503, 504}

SYSTEM_PROMPT = (
    "Você é um assistente virtual prestativo em um chatbot web. "
    "Responda de forma clara e objetiva, no mesmo idioma da mensagem do usuário. "
    "A interface não renderiza Markdown, então não use formatação como **negrito**, # títulos ou tabelas; "
    "para listas, use linhas começando com hífen. "
    "Use a ortografia correta do idioma, com acentos."
)


class AIServiceError(Exception):
    """Falha ao obter uma resposta da API de IA."""


@cache
def get_client() -> genai.Client:
    # Criado sob demanda para que a aplicação (e os testes) inicie mesmo sem chave configurada
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise AIServiceError("GEMINI_API_KEY não configurada no backend/.env")
    return genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=TIMEOUT_MS))


def build_contents(message: str, history: list[ChatMessage]) -> list[types.Content]:
    """Converte o histórico para o formato do Gemini, que usa o papel "model" no lugar de "assistant"."""
    contents = [
        types.Content(
            role="model" if item.role == "assistant" else "user",
            parts=[types.Part(text=item.content)],
        )
        for item in history
    ]
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))
    return contents


def get_models() -> list[str]:
    models = os.getenv("GEMINI_MODELS", DEFAULT_MODELS)
    return [model.strip() for model in models.split(",") if model.strip()]


async def generate_reply(message: str, history: list[ChatMessage]) -> str:
    """Envia a mensagem (com o histórico da conversa como contexto) ao Gemini e retorna a resposta."""
    client = get_client()
    contents = build_contents(message, history)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    error = AIServiceError("Nenhum modelo configurado em GEMINI_MODELS")
    for model in get_models():
        try:
            response = await client.aio.models.generate_content(model=model, contents=contents, config=config)
        except errors.APIError as exc:
            error = AIServiceError(f"Erro da API do Gemini em {model} ({exc.code}): {exc.message}")
            if exc.code not in RETRYABLE_STATUS_CODES:
                raise error from exc  # ex.: chave inválida — outro modelo não resolveria
        except Exception as exc:  # timeout, falha de rede etc.
            error = AIServiceError(f"Não foi possível contatar a API do Gemini em {model}: {exc!r}")
        else:
            if not response.text:
                # Pode acontecer quando a resposta é bloqueada pelos filtros de segurança
                raise AIServiceError(f"A API do Gemini retornou uma resposta vazia ({model})")
            return response.text.strip()
        logger.warning("%s", error)

    raise error
