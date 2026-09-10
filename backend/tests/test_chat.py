import asyncio
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from google.genai import errors

from app import main
from app.schemas import ChatMessage
from app.services import ai_service
from app.services.ai_service import AIServiceError

# Os testes nunca chamam a API real do Gemini: a IA é substituída por funções falsas.

client = TestClient(main.app)


@pytest.fixture
def fake_ai(monkeypatch):
    """Substitui a IA por uma resposta fixa e registra os argumentos recebidos."""
    calls = []

    async def fake_generate_reply(message, history):
        calls.append((message, history))
        return "Resposta da IA"

    monkeypatch.setattr(main, "generate_reply", fake_generate_reply)
    return calls


def make_fake_client(generate_content):
    return SimpleNamespace(aio=SimpleNamespace(models=SimpleNamespace(generate_content=generate_content)))


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_ai_reply(fake_ai):
    history = [
        {"role": "user", "content": "Oi"},
        {"role": "assistant", "content": "Olá! Como posso ajudar?"},
    ]
    response = client.post("/chat", json={"message": "  Me conte uma piada  ", "history": history})

    assert response.status_code == 200
    assert response.json() == {"reply": "Resposta da IA"}
    message, received_history = fake_ai[0]
    assert message == "Me conte uma piada"
    assert [(m.role, m.content) for m in received_history] == [
        ("user", "Oi"),
        ("assistant", "Olá! Como posso ajudar?"),
    ]


def test_chat_returns_502_when_ai_fails(monkeypatch):
    async def failing_generate_reply(message, history):
        raise AIServiceError("quota excedida")

    monkeypatch.setattr(main, "generate_reply", failing_generate_reply)
    response = client.post("/chat", json={"message": "Oi"})

    assert response.status_code == 502
    # O detalhe interno do erro não é exposto ao cliente
    assert response.json() == {"detail": "Falha ao obter resposta da IA"}


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"message": ""},
        {"message": "   "},
        {"message": "Oi", "history": [{"role": "system", "content": "x"}]},
    ],
)
def test_chat_rejects_invalid_payload(fake_ai, payload):
    response = client.post("/chat", json=payload)
    assert response.status_code == 422
    assert fake_ai == []


def test_build_contents_maps_roles_to_gemini_format():
    history = [
        ChatMessage(role="user", content="Oi"),
        ChatMessage(role="assistant", content="Olá!"),
    ]
    contents = ai_service.build_contents("Tudo bem?", history)

    assert [(c.role, c.parts[0].text) for c in contents] == [
        ("user", "Oi"),
        ("model", "Olá!"),
        ("user", "Tudo bem?"),
    ]


def test_generate_reply_returns_model_text(monkeypatch):
    async def generate_content(**kwargs):
        return SimpleNamespace(text="  Olá, tudo ótimo!  ")

    monkeypatch.setattr(ai_service, "get_client", lambda: make_fake_client(generate_content))
    assert asyncio.run(ai_service.generate_reply("Oi", [])) == "Olá, tudo ótimo!"


async def empty_reply(**kwargs):
    return SimpleNamespace(text=None)


async def network_error(**kwargs):
    raise TimeoutError("timeout")


@pytest.mark.parametrize("generate_content", [empty_reply, network_error])
def test_generate_reply_raises_ai_service_error(monkeypatch, generate_content):
    monkeypatch.setattr(ai_service, "get_client", lambda: make_fake_client(generate_content))
    with pytest.raises(AIServiceError):
        asyncio.run(ai_service.generate_reply("Oi", []))


def gemini_error(code):
    return errors.APIError(code, {"error": {"code": code, "message": "erro simulado"}})


def test_generate_reply_falls_back_to_next_model_when_overloaded(monkeypatch):
    models_tried = []

    async def generate_content(model, **kwargs):
        models_tried.append(model)
        if model == "modelo-principal":
            raise gemini_error(503)
        return SimpleNamespace(text="Resposta do modelo reserva")

    monkeypatch.setenv("GEMINI_MODELS", "modelo-principal, modelo-reserva")
    monkeypatch.setattr(ai_service, "get_client", lambda: make_fake_client(generate_content))

    assert asyncio.run(ai_service.generate_reply("Oi", [])) == "Resposta do modelo reserva"
    assert models_tried == ["modelo-principal", "modelo-reserva"]


def test_generate_reply_does_not_fall_back_on_permanent_errors(monkeypatch):
    models_tried = []

    async def generate_content(model, **kwargs):
        models_tried.append(model)
        raise gemini_error(400)  # ex.: chave inválida

    monkeypatch.setenv("GEMINI_MODELS", "modelo-principal,modelo-reserva")
    monkeypatch.setattr(ai_service, "get_client", lambda: make_fake_client(generate_content))

    with pytest.raises(AIServiceError, match="400"):
        asyncio.run(ai_service.generate_reply("Oi", []))
    assert models_tried == ["modelo-principal"]


def test_get_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    ai_service.get_client.cache_clear()
    with pytest.raises(AIServiceError, match="GEMINI_API_KEY"):
        ai_service.get_client()
    ai_service.get_client.cache_clear()
