const API = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const api = {
  dashboard: () => request("/dashboard/summary"),
  sla: () => request("/dashboard/sla"),
  renewals: () => request("/dashboard/renewals"),
  incentives: () => request("/dashboard/incentives"),
  profiles: (id) => request(`/profiles/${id}`),
  createProfile: (data) => request("/profiles", { method: "POST", body: JSON.stringify(data) }),
  approvalMap: (profileId) => request(`/approvals/map/${profileId}`),
  approvalDocs: (approvalId) => request(`/approvals/${approvalId}/documents`),
  applications: () => request("/applications"),
  createApplication: (data) => request("/applications", { method: "POST", body: JSON.stringify(data) }),
  workflow: (id) => request(`/applications/${id}/workflow`),
  validateDocument: (data) => request("/documents/validate", { method: "POST", body: JSON.stringify(data) })
};
