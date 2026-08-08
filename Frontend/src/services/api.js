const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Request failed");
  }

  return response.json();
}

export const api = {
  health: () => request("/health"),

  products: () => request("/api/products"),

  transactions: () => request("/api/transactions"),

  todayReport: () => request("/api/reports/today"),

  lowStock: () => request("/api/reports/low-stock"),

  processVoice: (audioBlob) => {
    const formData = new FormData();

    formData.append(
      "audio",
      audioBlob,
      "voice-command.webm"
    );

    return request("/api/voice/process", {
      method: "POST",
      body: formData,
    });
  },
};