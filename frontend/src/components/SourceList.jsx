import { useState } from "react";

export default function SourceList({ sources }) {
  const [expanded, setExpanded] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="source-list">
      <button
        className="source-list__toggle"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? "Ocultar" : "Ver"} fontes ({sources.length})
      </button>
      {expanded && (
        <ul className="source-list__items">
          {sources.map((src, i) => (
            <li key={i} className="source-list__item">
              {src.document}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
