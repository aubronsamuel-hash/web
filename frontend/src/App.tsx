import React from "react";
import { Outlet, Link, useNavigate, useLocation } from "react-router-dom";
import { isAuthenticated, logout } from "./lib/auth";

export default function App() {
  const nav = useNavigate();
  const loc = useLocation();
  const authed = isAuthenticated();

  React.useEffect(() => { if (!authed && loc.pathname !== "/login") nav("/login"); }, [authed, loc.pathname, nav]);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white shadow">
        <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
          <h1 className="font-bold">Coulisses Crew</h1>
          <nav className="space-x-4">
            <Link className="hover:underline" to="/">Dashboard</Link>
            <Link className="hover:underline" to="/users">Users</Link>
            <Link className="hover:underline" to="/intermittents">Intermittents</Link>
            {authed && (
              <button className="ml-4 px-3 py-1 rounded bg-gray-200 hover:bg-gray-300" onClick={() => { logout(); nav("/login"); }}>Se deconnecter</button>
            )}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl p-4">
        <Outlet />
      </main>
    </div>
  );
}
