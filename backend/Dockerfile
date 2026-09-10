FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências antes de copiar o código para aproveitar o cache de camadas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# As variáveis (GEMINI_API_KEY etc.) vêm do backend/.env via docker compose, não da imagem
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
