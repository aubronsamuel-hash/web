// @vitest-environment jsdom
import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import "@testing-library/jest-dom/vitest";
import MissionForm, { normalize } from "./MissionForm";
import Missions from "./Missions";

function mockFetchOnce(status: number, body: any) {
  (global as any).fetch = vi.fn().mockResolvedValue({ ok: status >= 200 && status < 300, status, json: async () => body, text: async () => JSON.stringify(body) });
}

describe("MissionForm", () => {
  beforeEach(() => { localStorage.setItem("cc_token","T"); vi.restoreAllMocks(); });
  it("OK: normalize renseigne ISO", () => {
    const out = normalize({ title:"A", start_at:"", end_at:"" });
    expect(out.start_at).toMatch(/T/);
    expect(out.end_at).toMatch(/T/);
  });
});

describe("Missions list", () => {
  beforeEach(() => { localStorage.setItem("cc_token","T"); vi.restoreAllMocks(); });
  it("OK: render list + bouton publier", async () => {
    mockFetchOnce(200, { items:[{ id:1, title:"A", start_at:new Date().toISOString(), end_at:new Date().toISOString(), status:"draft" }], total:1, page:1, size:10, pages:1 });
    render(<MemoryRouter><Missions /></MemoryRouter>);
    await waitFor(() => expect(screen.getByText("A")).toBeInTheDocument());
  });
  it("KO: API 401 -> message", async () => {
    (global as any).fetch = vi.fn().mockResolvedValue({ ok:false, status:401, text: async () => "Unauthorized" });
    render(<MemoryRouter><Missions /></MemoryRouter>);
    await waitFor(() => expect(screen.getByText(/401/)).toBeInTheDocument());
  });
});

