// @vitest-environment jsdom
import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import Intermittents from "./Intermittents";

function mockFetchOnce(status: number, body: any) {
  (global as any).fetch = vi.fn().mockResolvedValue({ ok: status >= 200 && status < 300, status, json: async () => body, text: async () => JSON.stringify(body) });
}

describe("Intermittents page", () => {
  beforeEach(() => {
    const store: Record<string, string> = {};
    (global as any).localStorage = {
      getItem: (k: string) => (k in store ? store[k] : null),
      setItem: (k: string, v: string) => { store[k] = v; },
      removeItem: (k: string) => { delete store[k]; },
      clear: () => { for (const k in store) delete store[k]; }
    };
    localStorage.setItem("cc_token", "T");
    vi.restoreAllMocks();
  });

  it("OK: affiche une ligne depuis API", async () => {
    mockFetchOnce(200, { items: [{ id:1, email:"a@ex.com", is_active:true }], total:1, page:1, size:20, pages:1 });
    render(<Intermittents />);
    await waitFor(() => expect(screen.getByText("a@ex.com")).toBeInTheDocument());
  });

  it("KO: 401 -> message d'erreur", async () => {
    (global as any).fetch = vi.fn().mockResolvedValue({ ok:false, status:401, text: async () => "Unauthorized" });
    render(<Intermittents />);
    await waitFor(() => expect(screen.getByText(/401/)).toBeInTheDocument());
  });
});
