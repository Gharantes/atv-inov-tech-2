function TypingIndicator() {
  return (
    <div className="message message--bot" aria-live="polite" aria-label="A IA está digitando">
      <div className="avatar avatar--bot avatar--small" aria-hidden="true">
        IA
      </div>
      <div className="bubble typing">
        <span />
        <span />
        <span />
      </div>
    </div>
  )
}

export default TypingIndicator
