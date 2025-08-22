import { describe, it, expect, beforeEach, vi } from "vitest";
import { login, isAuthenticated, logout } from "./auth";

function mockFetchOnce(status: number, body: any) {
  global.fetch = vi.fn().mockResolvedValue({ ok: status >= 200 && status < 300, status, json: async () => body }) as any;
}

describe("auth", () => {
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
  it("OK: login et stockage token", async () => {
    mockFetchOnce(200, { access_token: "T" });
    await login("a@b.com", "x");
    expect(isAuthenticated()).toBe(true);
  });
  it("KO: mauvais mdp -> erreur", async () => {
    mockFetchOnce(401, {});
    await expect(login("a@b.com", "bad")).rejects.toThrow();
    expect(isAuthenticated()).toBe(false);
  });
});
