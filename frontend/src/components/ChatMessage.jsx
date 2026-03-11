import AgentBadge from "./AgentBadge";
import SourceList from "./SourceList";

export default function ChatMessage({ message }) {
  if (message.type === "question") {
    return (
      <div className="chat-message chat-message--question">
        <p>{message.text}</p>
      </div>
    );
  }

  return (
    <div className="chat-message chat-message--answer">
      <div className="chat-message__header">
        <AgentBadge classification={message.classification} />
      </div>
      <p>{message.text}</p>
      <SourceList sources={message.sources} />
    </div>
  );
}
