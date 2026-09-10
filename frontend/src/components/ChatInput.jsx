import { useEffect, useRef, useState } from 'react'

function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  // Ajusta a altura do campo conforme o texto cresce
  useEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) return
    textarea.style.height = 'auto'
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`
    textarea.style.overflowY = textarea.scrollHeight > 160 ? 'auto' : 'hidden'
  }, [value])

  // Devolve o foco ao campo quando a resposta chega
  useEffect(() => {
    if (!disabled) textareaRef.current?.focus()
  }, [disabled])

  const canSend = value.trim().length > 0 && !disabled

  function handleSubmit(event) {
    event.preventDefault()
    if (!canSend) return
    onSend(value.trim())
    setValue('')
  }

  function handleKeyDown(event) {
    // Enter envia; Shift+Enter quebra linha
    if (event.key === 'Enter' && !event.shiftKey) {
      handleSubmit(event)
    }
  }

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <textarea
        ref={textareaRef}
        className="chat-input__field"
        placeholder="Digite sua mensagem..."
        aria-label="Mensagem"
        rows={1}
        value={value}
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
      />
      <button type="submit" className="button button--primary" disabled={!canSend}>
        Enviar
      </button>
    </form>
  )
}

export default ChatInput
