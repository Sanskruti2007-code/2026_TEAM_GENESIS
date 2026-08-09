const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api"
).replace(/\/$/, "");

const AI_SETTINGS_URL = `${API_BASE_URL}/api/settings/ai`;

async function handleResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message =
      data.detail ||
      data.message ||
      "AI settings request failed"

    throw new Error(message);
  }

  return data;
}

export async function getAIKeyStatus() {
  const response = await fetch(AI_SETTINGS_URL, {
    method: "GET",
  });

  return handleResponse(response);
}

export async function saveAIKey(provider, apiKey) {
  const response = await fetch(AI_SETTINGS_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      provider,
      api_key: apiKey,
    }),
  });

  return handleResponse(response);
}

export async function deleteAIKey(provider) {
  const response = await fetch(
    `${AI_SETTINGS_URL}/${provider}`,
    {
      method: "DELETE",
    }
  );

  return handleResponse(response);
}