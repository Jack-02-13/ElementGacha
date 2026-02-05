from __future__ import annotations

import base64
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# WARNING: Do NOT commit a real private key to git.
PRIVATE_KEY_B64 = "PASTE_PRIVATE_KEY_BASE64_HERE"


def decode_b64(value: str) -> bytes:
    padded = value.strip() + "=" * (-len(value.strip()) % 4)
    return base64.b64decode(padded, validate=True)


def canonical_payload_bytes(data: dict[str, Any]) -> bytes:
    payload = dict(data)
    payload.pop("sig", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return canonical.encode("utf-8")


def build_license() -> dict[str, Any]:
    return {
        "v": 1,
        "product": "ElementGacha",
        "license_id": str(uuid.uuid4()),
        "issued_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "features": {"paid": True},
    }


def sign_license(data: dict[str, Any]) -> dict[str, Any]:
    key_raw = decode_b64(PRIVATE_KEY_B64)
    private_key = Ed25519PrivateKey.from_private_bytes(key_raw)
    signature = private_key.sign(canonical_payload_bytes(data))
    signed = dict(data)
    signed["sig"] = base64.b64encode(signature).decode("ascii")
    return signed


def main() -> None:
    license_data = build_license()
    signed = sign_license(license_data)
    out_path = Path("license.json")
    out_path.write_text(json.dumps(signed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path.resolve()}")


if __name__ == "__main__":
    main()
