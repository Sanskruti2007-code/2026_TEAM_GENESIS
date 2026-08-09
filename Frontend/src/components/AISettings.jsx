import { useEffect, useState } from "react";

import {
  deleteAIKey,
  getAIKeyStatus,
  saveAIKey,
} from "../services/aiSettings";

import "./AISettings.css";

const PROVIDERS = {
  gemini: {
    name: "Gemini",
    description: "AI command understanding and voice fallback",
    placeholder: "Enter your Gemini API key",
  },
  openai: {
    name: "OpenAI",
    description: "Accurate voice command transcription",
    placeholder: "Enter your OpenAI API key",
  },
};

export default function AISettings() {
  const [selectedProvider, setSelectedProvider] =
    useState("gemini");

  const [apiKey, setApiKey] = useState("");

  const [keyStatus, setKeyStatus] = useState({
    gemini: false,
    openai: false,
  });

  const [loadingStatus, setLoadingStatus] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [notice, setNotice] = useState(null);

  const selectedProviderDetails =
    PROVIDERS[selectedProvider];

  useEffect(() => {
    let componentActive = true;

    async function loadKeyStatus() {
      try {
        const status = await getAIKeyStatus();

        if (componentActive) {
          setKeyStatus(status);
        }
      } catch (error) {
        if (componentActive) {
          setNotice({
            type: "error",
            text: error.message,
          });
        }
      } finally {
        if (componentActive) {
          setLoadingStatus(false);
        }
      }
    }

    loadKeyStatus();

    return () => {
      componentActive = false;
    };
  }, []);

  function selectProvider(provider) {
    setSelectedProvider(provider);
    setApiKey("");
    setNotice(null);
  }

  async function handleSave(event) {
    event.preventDefault();

    const cleanedKey = apiKey.trim();

    if (cleanedKey.length < 10) {
      setNotice({
        type: "error",
        text: "Please enter a valid API key.",
      });
      return;
    }

    setProcessing(true);
    setNotice(null);

    try {
      const result = await saveAIKey(
        selectedProvider,
        cleanedKey
      );

      setKeyStatus(result.status);
      setApiKey("");

      setNotice({
        type: "success",
        text: result.message,
      });
    } catch (error) {
      setNotice({
        type: "error",
        text: error.message,
      });
    } finally {
      setProcessing(false);
    }
  }

  async function handleRemove() {
    setProcessing(true);
    setNotice(null);

    try {
      const result = await deleteAIKey(
        selectedProvider
      );

      setKeyStatus(result.status);
      setApiKey("");

      setNotice({
        type: result.success ? "success" : "info",
        text: result.message,
      });
    } catch (error) {
      setNotice({
        type: "error",
        text: error.message,
      });
    } finally {
      setProcessing(false);
    }
  }

  return (
    <section className="ai-settings-card">
      <div className="ai-settings-header">
        <div>
          <p className="ai-settings-label">
            Secure AI Configuration
          </p>

          <h2>AI API Settings</h2>

          <p>
            Connect your preferred AI provider for voice
            commands and business automation.
          </p>
        </div>

        <span className="session-badge">
          Session only
        </span>
      </div>

      <div className="provider-options">
        {Object.entries(PROVIDERS).map(
          ([providerId, provider]) => {
            const configured = keyStatus[providerId];
            const selected =
              selectedProvider === providerId;

            return (
              <button
                key={providerId}
                type="button"
                className={`provider-option ${
                  selected ? "active" : ""
                }`}
                onClick={() =>
                  selectProvider(providerId)
                }
                aria-pressed={selected}
              >
                <div className="provider-option-top">
                  <strong>{provider.name}</strong>

                  <span
                    className={`provider-status ${
                      configured
                        ? "configured"
                        : "not-configured"
                    }`}
                  >
                    {loadingStatus
                      ? "Checking..."
                      : configured
                        ? "Connected"
                        : "Not connected"}
                  </span>
                </div>

                <small>{provider.description}</small>
              </button>
            );
          }
        )}
      </div>

      <form
        className="api-key-form"
        onSubmit={handleSave}
      >
        <label htmlFor="ai-api-key">
          {selectedProviderDetails.name} API Key
        </label>

        <input
          id="ai-api-key"
          name={`${selectedProvider}-api-key`}
          type="password"
          value={apiKey}
          placeholder={
            selectedProviderDetails.placeholder
          }
          onChange={(event) =>
            setApiKey(event.target.value)
          }
          autoComplete="off"
          spellCheck="false"
          disabled={processing}
        />

        <p className="api-key-help">
          Your key is temporarily stored in backend memory
          and is never returned by the API.
        </p>

        <div className="ai-settings-actions">
          <button
            type="submit"
            className="save-api-key-button"
            disabled={processing || !apiKey.trim()}
          >
            {processing ? "Please wait..." : "Save API Key"}
          </button>

          {keyStatus[selectedProvider] && (
            <button
              type="button"
              className="remove-api-key-button"
              onClick={handleRemove}
              disabled={processing}
            >
              Remove Key
            </button>
          )}
        </div>
      </form>

      {notice && (
        <p
          className={`ai-settings-notice ${notice.type}`}
          role={
            notice.type === "error"
              ? "alert"
              : "status"
          }
        >
          {notice.text}
        </p>
      )}

      <div className="api-key-security-note">
        Closing or restarting the backend automatically
        removes session API keys.
      </div>
    </section>
  );
}