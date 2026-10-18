// Base URL of the FastAPI backend. Override with VITE_API_URL in frontend/.env.local
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, options);
  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        message = body.detail;
      } else if (Array.isArray(body.detail)) {
        message = body.detail.map((d) => d.msg).join("; ");
      }
    } catch {
      // Response had no JSON body; keep the generic message.
    }
    throw new Error(message);
  }
  return response.json();
}

export function getWelcome() {
  return request("/");
}

export function getFlats() {
  return request("/flats");
}

export function getTotalArea() {
  return request("/total_area");
}

// `bills` is an object keyed by category: { security: {amount, file}, ... }
// Each category sends either a manual amount or an uploaded JPEG, never both.
export function submitBills(bills) {
  const formData = new FormData();
  for (const [category, { amount, file }] of Object.entries(bills)) {
    if (amount) {
      formData.append(`${category}_amount`, amount);
    } else if (file) {
      formData.append(`${category}_image`, file);
    }
  }
  return request("/bills/batch-submit", { method: "POST", body: formData });
}
