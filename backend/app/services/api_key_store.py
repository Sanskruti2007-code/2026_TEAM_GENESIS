from threading import Lock


class APIKeyStore:
    ALLOWED_PROVIDERS = {"gemini", "openai"}

    def __init__(self):
        # API keys sirf backend RAM mein rahengi.
        self._keys: dict[str, str] = {}
        self._lock = Lock()

    def _normalize_provider(self, provider: str) -> str:
        normalized = provider.strip().lower()

        if normalized not in self.ALLOWED_PROVIDERS:
            raise ValueError("Provider must be 'gemini' or 'openai'.")

        return normalized

    def set_key(self, provider: str, api_key: str) -> None:
        provider = self._normalize_provider(provider)
        api_key = api_key.strip()

        if not api_key:
            raise ValueError("API key cannot be empty.")

        with self._lock:
            self._keys[provider] = api_key

    def get_key(self, provider: str) -> str | None:
        provider = self._normalize_provider(provider)

        with self._lock:
            return self._keys.get(provider)

    def has_key(self, provider: str) -> bool:
        provider = self._normalize_provider(provider)

        with self._lock:
            return provider in self._keys

    def delete_key(self, provider: str) -> bool:
        provider = self._normalize_provider(provider)

        with self._lock:
            return self._keys.pop(provider, None) is not None

    def get_status(self) -> dict[str, bool]:
        with self._lock:
            return {
                provider: provider in self._keys
                for provider in sorted(self.ALLOWED_PROVIDERS)
            }

    def clear_all(self) -> None:
        with self._lock:
            self._keys.clear()


api_key_store = APIKeyStore()