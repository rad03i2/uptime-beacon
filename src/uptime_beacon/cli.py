from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .core import check_many

VERSION = "1.0.0"

def _targets(args) -> list[str]:
    values = list(args.urls)
    if args.file:
        try:
            values += [line.strip() for line in Path(args.file).read_text(encoding="utf-8").splitlines()
                       if line.strip() and not line.lstrip().startswith("#")]
        except OSError as exc:
            raise ValueError(f"Cannot read target file: {exc}") from exc
    seen = set()
    return [x for x in values if not (x in seen or seen.add(x))]

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="uptime-beacon", description="Check HTTP(S) endpoints for availability and latency.")
    p.add_argument("urls", nargs="*", help="HTTP(S) URLs to check")
    p.add_argument("-f", "--file", help="UTF-8 file containing one URL per line")
    p.add_argument("--timeout", type=float, default=10.0, help="request timeout in seconds (default: 10)")
    p.add_argument("--slow-ms", type=float, default=1500.0, help="mark responses above this latency as slow")
    p.add_argument("--method", choices=("HEAD", "GET"), default="HEAD")
    p.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    p.add_argument("--fail-on-slow", action="store_true", help="return failure when any endpoint is slow")
    p.add_argument("--version", action="version", version=f"uptime-beacon {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        urls = _targets(args)
        if not urls:
            raise ValueError("Provide at least one URL or --file")
        results = check_many(urls, timeout=args.timeout, slow_ms=args.slow_ms, method=args.method)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            state = "DOWN" if not r.ok else ("SLOW" if r.slow else "UP")
            detail = f"HTTP {r.status}" if r.status is not None else (r.error or "request failed")
            print(f"{state:4} {r.latency_ms:8.2f} ms  {detail:12}  {r.url}")
    failed = any(not r.ok or (args.fail_on_slow and r.slow) for r in results)
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
