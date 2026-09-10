// Serviço de chat — por enquanto usa respostas mock.
// Quando o backend (FastAPI) estiver pronto, basta trocar a implementação de
// `sendMessage` por uma chamada REST, mantendo a mesma assinatura:
//
//   const res = await fetch(`${API_URL}/chat`, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ message, history }),
//   })
//   if (!res.ok) throw new Error('Falha ao obter resposta da IA')
//   const data = await res.json()
//   return data.reply

const MOCK_RESPONSES = [
  {
    keywords: ['olá', 'ola', 'oi', 'bom dia', 'boa tarde', 'boa noite'],
    reply: 'Olá! 👋 Sou um assistente virtual. Como posso ajudar você hoje?',
  },
  {
    keywords: ['react'],
    reply:
      'React é uma biblioteca JavaScript para construir interfaces de usuário. Ela trabalha com componentes reutilizáveis e um DOM virtual, o que torna a atualização da tela eficiente.',
  },
  {
    keywords: ['python', 'fastapi'],
    reply:
      'FastAPI é um framework Python moderno para criar APIs. Ele é rápido, usa type hints para validação automática e gera documentação interativa em /docs.',
  },
  {
    keywords: ['ia', 'inteligência artificial', 'inteligencia artificial'],
    reply:
      'Inteligência Artificial é a área da computação que busca criar sistemas capazes de realizar tarefas que normalmente exigem inteligência humana, como entender linguagem, reconhecer imagens e tomar decisões.',
  },
  {
    keywords: ['piada'],
    reply: 'Por que o programador foi ao médico? Porque ele estava com muitos *bugs*! 🐛',
  },
  {
    keywords: ['obrigado', 'obrigada', 'valeu'],
    reply: 'Por nada! Se tiver mais alguma dúvida, é só perguntar. 😊',
  },
]

const FALLBACK_REPLIES = [
  'Interessante! Ainda estou em modo de demonstração, mas em breve poderei responder isso usando uma IA de verdade.',
  'Boa pergunta! No momento estou usando respostas simuladas enquanto o backend não fica pronto.',
  'Entendi sua mensagem. Quando a integração com a API de IA estiver concluída, darei uma resposta mais completa.',
]

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// Verifica se a palavra-chave aparece como palavra inteira (evita "ia" casar com "piada")
function containsWord(text, keyword) {
  return new RegExp(`(^|[^\\p{L}])${keyword}($|[^\\p{L}])`, 'u').test(text)
}

function findMockReply(message) {
  const text = message.toLowerCase()
  const match = MOCK_RESPONSES.find(({ keywords }) =>
    keywords.some((keyword) => containsWord(text, keyword)),
  )
  if (match) return match.reply
  return FALLBACK_REPLIES[Math.floor(Math.random() * FALLBACK_REPLIES.length)]
}

/**
 * Envia a mensagem do usuário e retorna a resposta da IA.
 * @param {string} message - Mensagem digitada pelo usuário.
 * @param {{ role: 'user' | 'assistant', content: string }[]} _history - Histórico da conversa
 *   (ainda não usado pelo mock; será enviado ao backend).
 * @returns {Promise<string>} Resposta gerada.
 */
export async function sendMessage(message, _history = []) {
  await wait(700 + Math.random() * 900)
  return findMockReply(message)
}
