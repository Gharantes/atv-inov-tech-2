function ChatHeader({ onClear, canClear }) {
  return (
    <header className="chat-header">
      <div className="chat-header__info">
        <div className="avatar avatar--bot" aria-hidden="true">
          IA
        </div>
        <div>
          <h1 className="chat-header__title">Chatbot IA</h1>
          <p className="chat-header__status">
            <span className="status-dot" aria-hidden="true" />
            Online
          </p>
        </div>
      </div>
      <button
        type="button"
        className="button button--ghost"
        onClick={onClear}
        disabled={!canClear}
      >
        Limpar conversa
      </button>
    </header>
  )
}

export default ChatHeader
