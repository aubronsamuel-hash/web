export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

function reqId() { return Math.random().toString(36).slice(2); }

export async function apiFetch<T>(
  path: string,
  opts: { method?: HttpMethod; body?: any; auth?: boolean; timeoutMs?: number } = {}
): Promise<T> {
  const base = import.meta.env.VITE_API_BASE || "http://localhost:8001";
  const url = `${base}${path}`;
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 5000);
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    [import.meta.env.VITE_REQUEST_ID_HEADER || "X-Request-ID"]: reqId()
  };
  if (opts.auth) {
    const token = localStorage.getItem("cc_token");
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(url, {
    method: opts.method || "GET",
    headers,
    body: opts.body ? JSON.stringify(opts.body) : undefined,
    signal: ctrl.signal
  });
  clearTimeout(t);
  if (!res.ok) {
    const msg = await safeText(res);
    throw new Error(`${res.status} ${msg}`);
  }
  return (await res.json()) as T;
}

async function safeText(res: Response): Promise<string> {
  try { return await res.text(); } catch { return ""; }
}
