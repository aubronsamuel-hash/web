import React from "react";
import { useNavigate } from "react-router-dom";
import { login, isAuthenticated } from "../lib/auth";

export default function Login() {
  const [email, setEmail] = React.useState("admin@example.com");
  const [password, setPassword] = React.useState("admin");
  const [err, setErr] = React.useState<string | null>(null);
  const nav = useNavigate();

  React.useEffect(() => {
    if (isAuthenticated()) nav("/");
  }, [nav]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      await login(email, password);
      nav("/");
    } catch (ex: any) {
      setErr(ex?.message || "Erreur de connexion");
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-16 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Connexion</h2>
      {err && <div className="mb-3 text-red-600 text-sm">{err}</div>}
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          className="w-full border px-3 py-2 rounded"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          className="w-full border px-3 py-2 rounded"
          placeholder="Mot de passe"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button className="w-full bg-gray-900 text-white py-2 rounded">Se connecter</button>
      </form>
    </div>
  );
}
