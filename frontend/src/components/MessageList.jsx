import { useEffect, useRef } from 'react'
import Message from './Message.jsx'
import TypingIndicator from './TypingIndicator.jsx'

const SUGGESTIONS = [
  'O que é Inteligência Artificial?',
  'Me explique o que é React',
  'Para que serve o FastAPI?',
  'Me conte uma piada',
]

function EmptyState({ onSuggestion }) {
  return (
    <div className="empty-state">
      <div className="avatar avatar--bot avatar--large" aria-hidden="true">
        IA
      </div>
      <h2>Como posso ajudar?</h2>
      <p>Digite uma pergunta abaixo ou escolha uma das sugestões.</p>
      <div className="suggestions">
        {SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            type="button"
            className="suggestion"
            onClick={() => onSuggestion(suggestion)}
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  )
}

function MessageList({ messages, isLoading, onSuggestion }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  if (messages.length === 0 && !isLoading) {
    return (
      <main className="message-list">
        <EmptyState onSuggestion={onSuggestion} />
      </main>
    )
  }

  return (
    <main className="message-list" aria-live="polite">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={endRef} />
    </main>
  )
}

export default MessageList
