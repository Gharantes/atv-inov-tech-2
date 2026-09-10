import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse
from app.services.ai_service import AIServiceError, generate_reply

# Carrega as variáveis de backend/.env (GEMINI_API_KEY etc.)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logger = logging.getLogger(__name__)

# Origens autorizadas a chamar a API (o Vite roda em localhost:5173 por padrão)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI(
    title="Chatbot IA",
    description="API do chatbot: recebe a mensagem do usuário e devolve a resposta da IA.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        reply = await generate_reply(request.message, request.history)
    except AIServiceError as exc:
        # O detalhe fica no log do servidor; o cliente recebe uma mensagem genérica
        logger.error("Falha ao gerar resposta: %s", exc)
        raise HTTPException(status_code=502, detail="Falha ao obter resposta da IA") from exc
    return ChatResponse(reply=reply)
