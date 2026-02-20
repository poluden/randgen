from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class GenResult:
    ts_iso: str
    ts_ms: int
    nonce: str
    rand_a: int
    calc_b: int


def _now_ms() -> int:
    return int(time.time() * 1000)


def _iso_utc(ms: int) -> str:
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def generate(seed_hint: str | None = None) -> GenResult:
    """
    Stateless генератор:
    - rand_a: crypto random 0..999999
    - calc_b: псевдо-детермінований через sha256(ts_ms + nonce + seed_hint)
    """
    ts_ms = _now_ms()
    nonce = secrets.token_hex(8)  # 16 hex chars
    rand_a = secrets.randbelow(1_000_000)

    base = f"{ts_ms}:{nonce}:{seed_hint or ''}".encode("utf-8")
    digest = hashlib.sha256(base).digest()

    # Формула: беремо 4 байти -> int, додаємо rand_a, modulo 1_000_000
    x = int.from_bytes(digest[:4], "big")
    calc_b = (x + rand_a * 2654435761) % 1_000_000  # Knuth multiplicative-ish

    return GenResult(
        ts_iso=_iso_utc(ts_ms),
        ts_ms=ts_ms,
        nonce=nonce,
        rand_a=rand_a,
        calc_b=calc_b,
    )