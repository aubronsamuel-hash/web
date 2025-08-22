import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { apiFetch } from "../lib/api";

type Mission = {
  id?: number;
  title: string;
  description?: string | null;
  location?: string | null;
  start_at: string;
  end_at: string;
  status?: string;
};

export default function MissionForm(){
  const params = useParams();
  const nav = useNavigate();
  const [model, setModel] = React.useState<Mission>({ title:"", description:"", location:"", start_at:"", end_at:"" });
  const [err, setErr] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);
  const isEdit = Boolean(params.id);

  React.useEffect(() => {
    async function fetchOne(){
      if (!isEdit) return;
      try {
        const r = await apiFetch<Mission>(`/missions/${params.id}`, { auth: true });
        setModel(r);
      } catch(e:any){ setErr(e?.message||"Erreur"); }
    }
    fetchOne();
  }, [isEdit, params.id]);

  async function onSubmit(e: React.FormEvent){
    e.preventDefault(); setErr(null); setLoading(true);
    try {
      const body = normalize(model);
      if (isEdit) await apiFetch(`/missions/${params.id}`, { method:"PUT", auth:true, body });
      else await apiFetch(`/missions`, { method:"POST", auth:true, body });
      nav("/missions");
    } catch(e:any){ setErr(e?.message||"Erreur enregistrement"); }
    finally { setLoading(false); }
  }

  return (
    <div className="max-w-xl">
      <h2 className="text-xl font-semibold mb-3">{isEdit?"Modifier":"Nouvelle"} mission</h2>
      {err && <div className="mb-2 text-red-600 text-sm">{err}</div>}
      <form onSubmit={onSubmit} className="bg-white p-4 rounded shadow space-y-3">
        <input className="w-full border px-3 py-2 rounded" placeholder="Titre" value={model.title} onChange={e=>setModel({...model,title:e.target.value})} required />
        <input className="w-full border px-3 py-2 rounded" placeholder="Lieu" value={model.location||""} onChange={e=>setModel({...model,location:e.target.value})} />
        <textarea className="w-full border px-3 py-2 rounded" placeholder="Description" value={model.description||""} onChange={e=>setModel({...model,description:e.target.value})} />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <label className="text-sm">Debut
            <input className="w-full border px-3 py-2 rounded" type="datetime-local" value={toLocalInput(model.start_at)} onChange={e=>setModel({...model,start_at:fromLocalInput(e.target.value)})} required />
          </label>
          <label className="text-sm">Fin
            <input className="w-full border px-3 py-2 rounded" type="datetime-local" value={toLocalInput(model.end_at)} onChange={e=>setModel({...model,end_at:fromLocalInput(e.target.value)})} required />
          </label>
        </div>
        <div className="flex gap-2">
          <button disabled={loading} className="bg-gray-900 text-white px-3 py-1 rounded">Enregistrer</button>
          <button type="button" className="px-3 py-1 rounded bg-gray-200" onClick={()=>nav("/missions")}>Annuler</button>
        </div>
      </form>
    </div>
  );
}

export function normalize(m: Mission){
  return {
    title: m.title,
    description: m.description || null,
    location: m.location || null,
    start_at: m.start_at || new Date().toISOString(),
    end_at: m.end_at || new Date(Date.now()+3600000).toISOString(),
  };
}

function toLocalInput(iso: string){
  if (!iso) return "";
  const d = new Date(iso);
  const pad=(n:number)=>String(n).padStart(2,"0");
  const y=d.getFullYear(), mo=pad(d.getMonth()+1), da=pad(d.getDate());
  const h=pad(d.getHours()), mi=pad(d.getMinutes());
  return `${y}-${mo}-${da}T${h}:${mi}`;
}
function fromLocalInput(v: string){
  if (!v) return "";
  // v est local "YYYY-MM-DDTHH:mm" -> ISO
  const d = new Date(v);
  return d.toISOString();
}

