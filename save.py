from __future__ import annotations

import json
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import config
import i18n


@dataclass
class SaveData:
    paid_unlocked: bool = False
    ticket_count: int = 0
    last_ticket_ts: float = 0.0
    total_draws: int = 0
    owned: dict[int, int] = field(default_factory=dict)
    ui_language: str = "zh"
    version: str = config.SAVE_VERSION

    def to_dict(self) -> dict[str, Any]:
        owned_serialized = {str(key): value for key, value in sorted(self.owned.items())}
        return {
            "paid_unlocked": self.paid_unlocked,
            "ticket_count": self.ticket_count,
            "last_ticket_ts": self.last_ticket_ts,
            "total_draws": self.total_draws,
            "owned": owned_serialized,
            "ui_language": self.ui_language,
            "version": self.version,
        }


def default_save(now: float | None = None) -> SaveData:
    current = time.time() if now is None else now
    return SaveData(last_ticket_ts=current)


def get_save_path() -> Path:
    config.SAVE_DIR.mkdir(parents=True, exist_ok=True)
    return config.SAVE_DIR / config.SAVE_FILENAME


def _normalize_owned(raw_owned: Any) -> dict[int, int]:
    if not isinstance(raw_owned, dict):
        return {}

    normalized: dict[int, int] = {}
    for key, value in raw_owned.items():
        try:
            atomic_number = int(key)
            count = int(value)
        except (TypeError, ValueError):
            continue
        if atomic_number < 1:
            continue
        normalized[atomic_number] = max(0, count)
    return normalized


def _build_save(payload: dict[str, Any], now: float) -> SaveData:
    return SaveData(
        paid_unlocked=bool(payload.get("paid_unlocked", payload.get("unlocked", False))),
        ticket_count=max(0, int(payload.get("ticket_count", 0))),
        last_ticket_ts=float(payload.get("last_ticket_ts", payload.get("last_free_pull_ts", now))),
        total_draws=max(0, int(payload.get("total_draws", payload.get("total_pulls", 0)))),
        owned=_normalize_owned(payload.get("owned", {})),
        ui_language=i18n.normalize_language(str(payload.get("ui_language", "zh"))),
        version=str(payload.get("version", config.SAVE_VERSION)),
    )


def load_save(path: Path | None = None, now: float | None = None) -> SaveData:
    current = time.time() if now is None else now
    save_path = path or get_save_path()
    if not save_path.exists():
        data = default_save(current)
        write_save(data, save_path)
        return data

    try:
        payload = json.loads(save_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = default_save(current)
        write_save(data, save_path)
        return data

    if not isinstance(payload, dict):
        data = default_save(current)
        write_save(data, save_path)
        return data

    return _build_save(payload, current)


def write_save(data: SaveData, path: Path | None = None) -> None:
    save_path = path or get_save_path()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(
        json.dumps(data.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_save(path: Path | None = None, now: float | None = None) -> SaveData:
    data = default_save(now)
    write_save(data, path)
    return data


def export_save(export_path: Path, path: Path | None = None) -> Path:
    save_path = path or get_save_path()
    if not save_path.exists():
        write_save(default_save(), save_path)
    export_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(save_path, export_path)
    return export_path


def import_save(import_path: Path, path: Path | None = None) -> Path:
    save_path = path or get_save_path()
    if not import_path.exists():
        raise FileNotFoundError(import_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(import_path, save_path)
    return save_path
