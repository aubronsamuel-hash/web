import React from "react";
import { apiFetch } from "../lib/api";

type User = { id: number; email: string; full_name?: string | null; is_active: boolean };

export default function Users() {
  const [items, setItems] = React.useState<User[]>([]);
  const [page, setPage] = React.useState(1);
  const [total, setTotal] = React.useState(0);
  const size = 10;

  React.useEffect(() => {
    apiFetch<{ items: User[]; total: number }>(`/users?page=${page}&size=${size}`, { auth: true })
      .then(r => { setItems(r.items); setTotal(r.total); })
      .catch(() => { setItems([]); setTotal(0); });
  }, [page]);

  const pages = Math.max(1, Math.ceil(total / size));

  return (
    <div>
      <h2 className="text-xl font-semibold mb-3">Users</h2>
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead><tr className="bg-gray-100 text-left"> <th className="p-2">ID</th><th className="p-2">Email</th><th className="p-2">Actif</th> </tr></thead>
          <tbody>
            {items.map(u => (
              <tr key={u.id} className="border-t">
                <td className="p-2">{u.id}</td>
                <td className="p-2">{u.email}</td>
                <td className="p-2">{u.is_active ? "oui" : "non"}</td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td className="p-2" colSpan={3}>Aucun utilisateur</td></tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-3 flex items-center gap-2">
        <button className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
          onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Prev</button>
        <span>Page {page} / {pages}</span>
        <button className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
          onClick={() => setPage(p => Math.min(pages, p + 1))} disabled={page >= pages}>Next</button>
      </div>
    </div>
  );
}
