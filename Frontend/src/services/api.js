const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/$/, "");

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers,
    });
  } catch {
    throw new Error(
      "Backend connect nahi hua. FastAPI ko port 8000 par start karo."
    );
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const validation = Array.isArray(data.detail)
      ? data.detail.map((item) => item.msg).join(", ")
      : data.detail;
    throw new Error(validation || data.message || "Request failed");
  }
  return data;
}

export const api = {
  health: () => request("/api/health"),

  products: () => request("/api/products"),
  createProduct: (product) =>
    request("/api/products", {
      method: "POST",
      body: JSON.stringify(product),
    }),
  updateProduct: (id, product) =>
    request(`/api/products/${id}`, {
      method: "PUT",
      body: JSON.stringify(product),
    }),
  deleteProduct: (id) =>
    request(`/api/products/${id}`, { method: "DELETE" }),

  transactions: () => request("/api/transactions"),
  createOrder: (order) =>
    request("/api/transactions", {
      method: "POST",
      body: JSON.stringify(order),
    }),

  todayReport: () => request("/api/reports/today"),
  lowStock: () => request("/api/reports/low-stock"),

  processText: (text, language = "mr-IN") =>
    request("/api/commands", {
      method: "POST",
      body: JSON.stringify({ text, language }),
    }),

  processVoice: (audioBlob, language = "mr-IN") => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "voice-command.webm");
    return request(
      `/api/voice/process?language=${encodeURIComponent(language)}`,
      { method: "POST", body: formData }
    );
  },
};
