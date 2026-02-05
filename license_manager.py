from __future__ import annotations

import base64
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

PUBLIC_KEY_B64 = "9fBzaDG+VBIkoAltzQCrG0ojQMRtKMfSdje6lJIcJNg="
LICENSE_FILENAME = "license.json"
PRODUCT_NAME = "ElementGacha"
SUPPORTED_VERSION = 1


def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _license_path() -> Path:
    return _app_dir() / LICENSE_FILENAME


def get_license_path() -> Path:
    return _license_path()


def _canonical_payload_bytes(data: dict[str, Any]) -> bytes:
    payload = dict(data)
    payload.pop("sig", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return canonical.encode("utf-8")


def _decode_b64(value: str) -> bytes:
    padded = value.strip() + "=" * (-len(value.strip()) % 4)
    return base64.b64decode(padded, validate=True)


def _load_public_key() -> Ed25519PublicKey:
    key_raw = _decode_b64(PUBLIC_KEY_B64)
    if len(key_raw) != 32:
        raise ValueError("public_key_invalid_length")
    return Ed25519PublicKey.from_public_bytes(key_raw)


def load_license() -> tuple[bool, str, dict[str, Any] | None]:
    path = _license_path()
    if not path.exists():
        return False, "license_not_found", None

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return False, "license_parse_error", None

    if not isinstance(data, dict):
        return False, "license_not_object", None

    for field in ("v", "product", "features", "sig"):
        if field not in data:
            return False, f"missing_field:{field}", None

    if data.get("v") != SUPPORTED_VERSION:
        return False, "version_mismatch", None
    if data.get("product") != PRODUCT_NAME:
        return False, "product_mismatch", None

    features = data.get("features")
    if not isinstance(features, dict):
        return False, "features_invalid", None
    if features.get("paid") is not True:
        return False, "paid_feature_missing", None

    sig_b64 = data.get("sig")
    if not isinstance(sig_b64, str):
        return False, "sig_not_string", None

    try:
        signature = _decode_b64(sig_b64)
    except Exception:
        return False, "sig_base64_invalid", None

    try:
        public_key = _load_public_key()
    except Exception:
        return False, "public_key_invalid", None

    payload = _canonical_payload_bytes(data)
    try:
        public_key.verify(signature, payload)
    except InvalidSignature:
        return False, "bad_signature", None
    except Exception:
        return False, "verify_error", None

    return True, "ok", data


def is_paid_unlocked() -> tuple[bool, str]:
    is_valid, reason, data = load_license()
    if not is_valid or data is None:
        return False, reason
    features = data.get("features", {})
    return bool(isinstance(features, dict) and features.get("paid") is True), reason


def install_license_from_path(source_path: str) -> tuple[bool, str]:
    src = Path(source_path.strip().strip('"').strip("'"))
    if not src.exists():
        return False, "source_not_found"
    if src.suffix.lower() != ".json":
        return False, "source_not_json"
    try:
        dst = _license_path()
        shutil.copy2(src, dst)
    except OSError:
        return False, "copy_failed"
    ok, reason, _ = load_license()
    return ok, reason
