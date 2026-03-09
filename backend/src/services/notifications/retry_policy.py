class RetryPolicyService:
    def __init__(self) -> None:
        self.max_retries = 2

    def should_retry(self, attempts: int, error_code: str) -> bool:
        return error_code == "transient_error" and attempts < self.max_retries


retry_policy_service = RetryPolicyService()
