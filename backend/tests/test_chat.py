import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.ai_service import FALLBACK_REPLIES

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Bom dia!", "Olá!"),
        ("Me explique o que é React", "React é"),
        ("Para que serve o FastAPI?", "FastAPI é"),
        ("O que é IA?", "Inteligência Artificial é"),
        ("Me conte uma piada", "programador"),
        ("Valeu!", "Por nada!"),
    ],
)
def test_chat_keyword_replies(message, expected):
    response = client.post("/chat", json={"message": message, "history": []})
    assert response.status_code == 200
    assert expected in response.json()["reply"]


def test_chat_matches_whole_words_only():
    # "média" contém "ia", mas não deve cair na resposta sobre IA
    response = client.post("/chat", json={"message": "Qual a média da turma?"})
    assert response.json()["reply"] in FALLBACK_REPLIES


def test_chat_accepts_history():
    history = [
        {"role": "user", "content": "Oi"},
        {"role": "assistant", "content": "Olá! Como posso ajudar?"},
    ]
    response = client.post("/chat", json={"message": "Me conte uma piada", "history": history})
    assert response.status_code == 200
    assert "programador" in response.json()["reply"]


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"message": ""},
        {"message": "   "},
        {"message": "Oi", "history": [{"role": "system", "content": "x"}]},
    ],
)
def test_chat_rejects_invalid_payload(payload):
    response = client.post("/chat", json=payload)
    assert response.status_code == 422
