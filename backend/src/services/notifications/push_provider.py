class PushProvider:
    def send(self, push_token: str, title: str, message: str) -> tuple[bool, str | None]:
        if push_token.startswith("invalid_"):
            return False, "invalid_token"
        if push_token.startswith("transient_"):
            return False, "transient_error"
        return True, None


push_provider = PushProvider()
