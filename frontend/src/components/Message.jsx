function formatTime(date) {
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function Message({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`message ${isUser ? 'message--user' : 'message--bot'}`}>
      {!isUser && (
        <div className="avatar avatar--bot avatar--small" aria-hidden="true">
          IA
        </div>
      )}
      <div className={`bubble ${message.error ? 'bubble--error' : ''}`}>
        <p className="bubble__text">{message.content}</p>
        <time className="bubble__time">{formatTime(message.createdAt)}</time>
      </div>
    </div>
  )
}

export default Message
