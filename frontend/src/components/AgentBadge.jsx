const LABELS = {
  rh: "Agente RH",
  tecnico: "Agente Técnico",
  both: "Ambos Agentes",
};

export default function AgentBadge({ classification }) {
  const label = LABELS[classification] || classification;
  return <span className={`agent-badge agent-badge--${classification}`}>{label}</span>;
}
