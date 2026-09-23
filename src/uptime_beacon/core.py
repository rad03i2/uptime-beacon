from __future__ import annotations

import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import urlparse

USER_AGENT = "uptime-beacon/1.0 (+https://github.com/rad03i2/uptime-beacon)"

@dataclass(frozen=True)
class CheckResult:
    url: str
    ok: bool
    status: int | None
    latency_ms: float
    checked_at: str
    error: str | None = None
    slow: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def validate_url(url: str) -> str:
    value = url.strip()
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"Invalid HTTP(S) URL: {url!r}")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed")
    return value


def check_url(url: str, *, timeout: float = 10.0, slow_ms: float = 1500.0,
              method: str = "HEAD") -> CheckResult:
    url = validate_url(url)
    if timeout <= 0 or slow_ms < 0:
        raise ValueError("timeout must be > 0 and slow_ms must be >= 0")
    method = method.upper()
    if method not in {"HEAD", "GET"}:
        raise ValueError("method must be HEAD or GET")
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    started = time.perf_counter()
    status = None
    error = None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.status
            ok = 200 <= status < 400
    except urllib.error.HTTPError as exc:
        status = exc.code
        ok = False
        error = f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        ok = False
        reason = getattr(exc, "reason", exc)
        error = f"{type(reason).__name__}: {reason}"
    elapsed = (time.perf_counter() - started) * 1000
    return CheckResult(url, ok, status, round(elapsed, 2),
                       datetime.now(timezone.utc).isoformat(), error, elapsed > slow_ms)


def check_many(urls: Iterable[str], **kwargs) -> list[CheckResult]:
    return [check_url(url, **kwargs) for url in urls]
