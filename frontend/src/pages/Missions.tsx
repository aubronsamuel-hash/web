import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";

type Mission = {
  id: number;
  title: string;
  description?: string | null;
  location?: string | null;
  start_at: string;
  end_at: string;
  status: string;
  published_at?: string | null;
};

type ListResp = { items: Mission[]; total: number; page: number; size: number; pages: number };

export default function Missions() {
  const [items, setItems] = React.useState<Mission[]>([]);
  const [page, setPage] = React.useState(1);
  const [total, setTotal] = React.useState(0);
  const [size] = React.useState(10);
  const [q, setQ] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [err, setErr] = React.useState<string | null>(null);
  const nav = useNavigate();

  async function load() {
    setLoading(true); setErr(null);
    const params = new URLSearchParams();
    params.set("page", String(page));
    params.set("size", String(size));
    if (q) params.set("q", q);
    try {
      const r = await apiFetch<ListResp>(`/missions?${params.toString()}`, { auth: true, timeoutMs: 8000 });
      setItems(r.items); setTotal(r.total);
    } catch (e: any) {
      setItems([]); setTotal(0); setErr(e?.message || "Erreur");
    } finally { setLoading(false); }
  }

  React.useEffect(() => { load(); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, [page]);

  function onSearch(e: React.FormEvent) { e.preventDefault(); setPage(1); load(); }

  async function action(id: number, kind: "publish"|"duplicate"|"delete") {
    try {
      if (kind === "publish") await apiFetch(`/missions/${id}/publish`, { method: "POST", auth: true });
      if (kind === "duplicate") await apiFetch(`/missions/${id}/duplicate`, { method: "POST", auth: true });
      if (kind === "delete") await apiFetch(`/missions/${id}`, { method: "DELETE", auth: true });
      await load();
    } catch (e: any) { setErr(e?.message || "Erreur action"); }
  }

  const pages = Math.max(1, Math.ceil(total / size));

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xl font-semibold">Missions</h2>
        <button
          className="bg-gray-900 text-white px-3 py-1 rounded"
          onClick={() => nav("/missions/new")}
        >Nouvelle</button>
      </div>
      <form onSubmit={onSearch} className="bg-white p-3 rounded shadow mb-3 flex gap-2">
        <input className="border px-2 py-1 rounded flex-1" placeholder="Recherche" value={q} onChange={e=>setQ(e.target.value)} />
        <button className="bg-gray-900 text-white px-3 py-1 rounded">Rechercher</button>
      </form>

      {err && <div className="mb-2 text-red-600 text-sm">{err}</div>}

      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="p-2">ID</th>
              <th className="p-2">Titre</th>
              <th className="p-2">Lieu</th>
              <th className="p-2">Debut</th>
              <th className="p-2">Fin</th>
              <th className="p-2">Statut</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map(m => (
              <tr key={m.id} className="border-t">
                <td className="p-2">{m.id}</td>
                <td className="p-2"><Link className="text-blue-700 hover:underline" to={`/missions/${m.id}`}>{m.title}</Link></td>
                <td className="p-2">{m.location || "-"}</td>
                <td className="p-2">{fmt(m.start_at)}</td>
                <td className="p-2">{fmt(m.end_at)}</td>
                <td className="p-2">{m.status}</td>
                <td className="p-2 space-x-2">
                  <button className="px-2 py-0.5 bg-gray-200 rounded disabled:opacity-50" disabled={m.status==="published"} onClick={()=>action(m.id,"publish")}>Publier</button>
                  <button className="px-2 py-0.5 bg-gray-200 rounded" onClick={()=>action(m.id,"duplicate")}>Dupliquer</button>
                  <button className="px-2 py-0.5 bg-red-200 rounded" onClick={()=>action(m.id,"delete")}>Supprimer</button>
                </td>
              </tr>
            ))}
            {(!loading && items.length === 0) && (
              <tr><td className="p-2" colSpan={7}>Aucune mission</td></tr>
            )}
            {loading && (<tr><td className="p-2" colSpan={7}>Chargement...</td></tr>)}
          </tbody>
        </table>
      </div>

      <div className="mt-3 flex items-center gap-2">
        <button className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50" onClick={()=>setPage(p=>Math.max(1,p-1))} disabled={page<=1}>Prev</button>
        <span>Page {page} / {pages}</span>
        <button className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50" onClick={()=>setPage(p=>Math.min(pages,p+1))} disabled={page>=pages}>Next</button>
      </div>
    </div>
  );
}

function fmt(s: string){ try { return new Date(s).toLocaleString(); } catch { return s; } }

