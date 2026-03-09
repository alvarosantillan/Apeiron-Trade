from typing import Protocol


class BaseProviderAdapter(Protocol):
    def validate_credentials(self, api_key: str) -> bool:
        ...

    def generate_decision(self, symbol: str, timeframe: str, prompt: str) -> dict:
        ...
