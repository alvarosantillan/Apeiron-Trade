from __future__ import annotations

from collections import defaultdict
from time import perf_counter


class PersistenceMetrics:
    def __init__(self) -> None:
        self.counters = defaultdict(int)
        self.latency_samples: list[float] = []

    def inc(self, name: str) -> None:
        self.counters[name] += 1

    def observe(self, seconds: float) -> None:
        self.latency_samples.append(seconds)

    def timed(self, name: str):
        start = perf_counter()

        class _Ctx:
            def __enter__(self_inner):
                return self_inner

            def __exit__(self_inner, exc_type, exc, tb):
                duration = perf_counter() - start
                self.observe(duration)
                self.inc(name)
                return False

        return _Ctx()


persistence_metrics = PersistenceMetrics()
