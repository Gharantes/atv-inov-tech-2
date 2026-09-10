import { useState } from 'react'
import ChatHeader from './components/ChatHeader.jsx'
import ChatInput from './components/ChatInput.jsx'
import MessageList from './components/MessageList.jsx'
import { sendMessage } from './services/chatService.js'
import './App.css'

function createMessage(role, content, extra = {}) {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    createdAt: new Date(),
    ...extra,
  }
}

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  async function handleSend(text) {
    const history = messages
      .filter((message) => !message.error)
      .map(({ role, content }) => ({ role, content }))

    setMessages((prev) => [...prev, createMessage('user', text)])
    setIsLoading(true)

    try {
      const reply = await sendMessage(text, history)
      setMessages((prev) => [...prev, createMessage('assistant', reply)])
    } catch {
      setMessages((prev) => [
        ...prev,
        createMessage('assistant', 'Não foi possível obter uma resposta. Tente novamente.', {
          error: true,
        }),
      ])
    } finally {
      setIsLoading(false)
    }
  }

  function handleClear() {
    setMessages([])
  }

  return (
    <div className="chat">
      <ChatHeader onClear={handleClear} canClear={messages.length > 0 && !isLoading} />
      <MessageList messages={messages} isLoading={isLoading} onSuggestion={handleSend} />
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  )
}

export default App
