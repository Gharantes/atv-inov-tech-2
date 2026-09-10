// Serviço de chat — envia a mensagem para o backend (FastAPI) via REST/JSON.
// A URL da API pode ser configurada com a variável de ambiente VITE_API_URL.

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

/**
 * Envia a mensagem do usuário e retorna a resposta da IA.
 * @param {string} message - Mensagem digitada pelo usuário.
 * @param {{ role: 'user' | 'assistant', content: string }[]} history - Histórico da conversa.
 * @returns {Promise<string>} Resposta gerada.
 */
export async function sendMessage(message, history = []) {
  const res = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
  })
  if (!res.ok) throw new Error(`Falha ao obter resposta da IA (HTTP ${res.status})`)
  const data = await res.json()
  return data.reply
}
