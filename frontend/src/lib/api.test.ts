import { describe, it, expect, vi, beforeEach } from "vitest";
import { apiFetch } from "./api";

describe("api", () => {
  beforeEach(() => {
    const store: Record<string, string> = {};
    // @ts-ignore
    global.localStorage = {
      getItem: k => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = v; },
      removeItem: k => { delete store[k]; },
      clear: () => { for (const k in store) delete store[k]; }
    };
    vi.restoreAllMocks();
  });
  it("OK: ajoute Authorization si token", async () => {
    localStorage.setItem("cc_token", "T");
    const spy = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ ok: 1 }) });
    global.fetch = spy as any;
    await apiFetch("/healthz", { auth: true });
    const args = (spy as any).mock.calls[0][1];
    expect(args.headers["Authorization"]).toContain("Bearer T");
  });
  it("KO: 401 remonte erreur", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false, status: 401, text: async () => "Unauthorized" }) as any;
    await expect(apiFetch("/users", { auth: true })).rejects.toThrow(/401/);
  });
});
