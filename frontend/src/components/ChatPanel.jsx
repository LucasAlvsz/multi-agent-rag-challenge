import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../api";
import ChatMessage from "./ChatMessage";

export default function ChatPanel() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e) {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { type: "question", text: question }]);
    setLoading(true);

    try {
      const data = await askQuestion(question);
      setMessages((prev) => [
        ...prev,
        {
          type: "answer",
          text: data.answer,
          classification: data.classification,
          sources: data.sources,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          type: "answer",
          text: `Erro: ${err.message}`,
          classification: "error",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-panel">
      <div className="chat-panel__messages">
        {messages.length === 0 && (
          <p className="chat-panel__empty">
            Faça uma pergunta sobre RH ou documentação técnica.
          </p>
        )}
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        {loading && (
          <div className="chat-message chat-message--answer chat-message--loading">
            <span className="loading-dots">Pensando</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-panel__form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Digite sua pergunta..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  );
}
