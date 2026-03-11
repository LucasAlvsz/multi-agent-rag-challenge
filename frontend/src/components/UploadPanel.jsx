import { useState } from "react";
import { uploadDocument } from "../api";

export default function UploadPanel() {
  const [content, setContent] = useState("");
  const [domain, setDomain] = useState("rh");
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!content.trim()) return;

    setStatus("loading");
    setResult(null);

    try {
      const data = await uploadDocument(content.trim(), domain);
      setStatus("success");
      setResult(data);
      setContent("");
    } catch (err) {
      setStatus("error");
      setResult({ message: err.message });
    }
  }

  return (
    <div className="upload-panel">
      <form className="upload-panel__form" onSubmit={handleSubmit}>
        <label htmlFor="doc-content">Conteúdo do documento</label>
        <textarea
          id="doc-content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Cole o texto do documento aqui..."
          rows={8}
        />

        <fieldset className="upload-panel__domain">
          <legend>Domínio</legend>
          <label>
            <input
              type="radio"
              name="domain"
              value="rh"
              checked={domain === "rh"}
              onChange={(e) => setDomain(e.target.value)}
            />
            RH
          </label>
          <label>
            <input
              type="radio"
              name="domain"
              value="tecnico"
              checked={domain === "tecnico"}
              onChange={(e) => setDomain(e.target.value)}
            />
            Técnico
          </label>
        </fieldset>

        <button type="submit" disabled={status === "loading" || !content.trim()}>
          {status === "loading" ? "Enviando..." : "Enviar documento"}
        </button>
      </form>

      {status === "success" && result && (
        <div className="upload-panel__result upload-panel__result--success">
          Documento indexado com sucesso.
          <br />
          <strong>ID:</strong> {result.doc_id} &nbsp;|&nbsp;
          <strong>Chunks:</strong> {result.chunks_count} &nbsp;|&nbsp;
          <strong>Domínio:</strong> {result.domain}
        </div>
      )}

      {status === "error" && result && (
        <div className="upload-panel__result upload-panel__result--error">
          Erro: {result.message}
        </div>
      )}
    </div>
  );
}
