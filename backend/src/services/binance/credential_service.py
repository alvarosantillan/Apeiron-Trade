from datetime import datetime, timezone


class BinanceCredentialStore:
    def __init__(self) -> None:
        self._by_user: dict[str, dict] = {}

    def upsert(self, user_id: str, api_key: str, secret_key: str) -> dict:
        if not api_key.startswith("bnc_") or not secret_key.startswith("sec_"):
            raise ValueError("invalid_credentials")

        record = {
            "api_key": api_key,
            "secret_key": secret_key,
            "active": True,
            "verified_at": datetime.now(timezone.utc),
        }
        self._by_user[user_id] = record
        return record

    def status(self, user_id: str) -> dict:
        record = self._by_user.get(user_id)
        if not record:
            return {"active": False, "api_key_suffix": None, "verified_at": None}

        return {
            "active": record["active"],
            "api_key_suffix": record["api_key"][-4:],
            "verified_at": record["verified_at"],
        }

    def has_active_credentials(self, user_id: str) -> bool:
        return self._by_user.get(user_id, {}).get("active", False)


credential_store = BinanceCredentialStore()
