import React from "react";
import { apiFetch } from "../lib/api";
import Pagination from "../components/Pagination";

type Intermittent = {
  id: number;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  phone?: string | null;
  skills?: string | null;
  is_active: boolean;
};

type ListResp = { items: Intermittent[]; total: number; page: number; size: number; pages: number };

export default function Intermittents() {
  const [items, setItems] = React.useState<Intermittent[]>([]);
  const [page, setPage] = React.useState(1);
  const [total, setTotal] = React.useState(0);
  const [size] = React.useState(20);
  const [q, setQ] = React.useState("");
  const [skill, setSkill] = React.useState("");
  const [active, setActive] = React.useState<string>("");
  const [loading, setLoading] = React.useState(false);
  const [err, setErr] = React.useState<string | null>(null);

  async function load() {
    setLoading(true); setErr(null);
    const params = new URLSearchParams();
    params.set("page", String(page));
    params.set("size", String(size));
    if (q) params.set("q", q);
    if (skill) params.set("skill", skill);
    if (active === "true" || active === "false") params.set("active", active);
    try {
      const r = await apiFetch<ListResp>(`/intermittents?${params.toString()}`, { auth: true, timeoutMs: 8000 });
      setItems(r.items); setTotal(r.total);
    } catch (e: any) {
      setItems([]); setTotal(0); setErr(e?.message || "Erreur");
    } finally { setLoading(false); }
  }

  React.useEffect(() => { load(); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, [page]);

  function onSearch(e: React.FormEvent) { e.preventDefault(); setPage(1); load(); }

  const pages = Math.max(1, Math.ceil(total / size));

  return (
    <div>
      <h2 className="text-xl font-semibold mb-3">Intermittents</h2>
      <form onSubmit={onSearch} className="bg-white p-3 rounded shadow mb-3 grid grid-cols-1 md:grid-cols-4 gap-2">
        <input className="border px-2 py-1 rounded" placeholder="Recherche (email/nom/skills)" value={q} onChange={e=>setQ(e.target.value)} />
        <input className="border px-2 py-1 rounded" placeholder="Skill (ex: son)" value={skill} onChange={e=>setSkill(e.target.value)} />
        <select className="border px-2 py-1 rounded" value={active} onChange={e=>setActive(e.target.value)}>
          <option value="">Actif: tous</option>
          <option value="true">Actifs</option>
          <option value="false">Inactifs</option>
        </select>
        <button className="bg-gray-900 text-white px-3 py-1 rounded">Rechercher</button>
      </form>

      {err && <div className="mb-2 text-red-600 text-sm">{err}</div>}

      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="p-2">ID</th>
              <th className="p-2">Email</th>
              <th className="p-2">Nom</th>
              <th className="p-2">Phone</th>
              <th className="p-2">Skills</th>
              <th className="p-2">Actif</th>
            </tr>
          </thead>
          <tbody>
            {items.map(it => (
              <tr key={it.id} className="border-t">
                <td className="p-2">{it.id}</td>
                <td className="p-2">{it.email}</td>
                <td className="p-2">{[it.first_name, it.last_name].filter(Boolean).join(" ")}</td>
                <td className="p-2">{it.phone || "-"}</td>
                <td className="p-2">{it.skills || "-"}</td>
                <td className="p-2">{it.is_active ? "oui" : "non"}</td>
              </tr>
            ))}
            {(!loading && items.length === 0) && (
              <tr><td className="p-2" colSpan={6}>Aucun intermittent</td></tr>
            )}
            {loading && (
              <tr><td className="p-2" colSpan={6}>Chargement...</td></tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-3">
        <Pagination page={page} pages={pages} onPrev={()=>setPage(p=>Math.max(1,p-1))} onNext={()=>setPage(p=>Math.min(pages,p+1))} />
      </div>
    </div>
  );
}
