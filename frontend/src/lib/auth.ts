export function isAuthenticated(): boolean {
  return Boolean(localStorage.getItem("cc_token"));
}

export function logout(): void {
  localStorage.removeItem("cc_token");
}

export async function login(email: string, password: string): Promise<void> {
  const base = import.meta.env.VITE_API_BASE || "http://localhost:8001";
  const res = await fetch(`${base}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password })
  });
  if (!res.ok) throw new Error("Identifiants invalides");
  const data = (await res.json()) as { access_token: string };
  localStorage.setItem("cc_token", data.access_token);
}
