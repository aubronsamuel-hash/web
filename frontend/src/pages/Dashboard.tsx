import React from "react";
import { apiFetch } from "../lib/api";

export default function Dashboard() {
  const [status, setStatus] = React.useState<string>("...");
  React.useEffect(() => {
    apiFetch<{ status: string }>("/healthz").then(r => setStatus(r.status)).catch(() => setStatus("KO"));
  }, []);
  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Dashboard</h2>
      <div className="p-3 rounded bg-white shadow inline-block">Healthz: {status}</div>
    </div>
  );
}
