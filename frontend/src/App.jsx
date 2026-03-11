import { useState } from "react";
import ChatPanel from "./components/ChatPanel";
import UploadPanel from "./components/UploadPanel";

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="app">
      <header className="app__header">
        <h1>RAG Multi-Agent</h1>
        <p>Sistema de consulta com agentes especializados em RH e documentação técnica</p>
      </header>

      <nav className="app__tabs">
        <button
          className={`tab ${activeTab === "chat" ? "tab--active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          Consulta
        </button>
        <button
          className={`tab ${activeTab === "upload" ? "tab--active" : ""}`}
          onClick={() => setActiveTab("upload")}
        >
          Ingestão
        </button>
      </nav>

      <main className="app__content">
        <div style={{ display: activeTab === "chat" ? "flex" : "none", flexDirection: "column", flex: 1 }}>
          <ChatPanel />
        </div>
        <div style={{ display: activeTab === "upload" ? "flex" : "none", flexDirection: "column", flex: 1 }}>
          <UploadPanel />
        </div>
      </main>
    </div>
  );
}
